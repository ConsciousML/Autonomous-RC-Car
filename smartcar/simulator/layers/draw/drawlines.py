from layers.layer import Layer
from utils.basic_objects import Circle, Point, RoadLine
from utils.colors import Yellow, White

import numpy as np
from PIL import ImageDraw

from math import atan2, pi, sqrt
from random import choice, gauss, randint, random


class DrawLines(Layer):
    '''This layer draws the border of the road (constituted of 2 lines.)'''

    def __init__(self, xy0_range=None,
                    xy1_range=None,
                    radius_range=None,
                    thickness_range=None,
                    color_range=None,
                    obstacle_color_ranges=None,
                    middle_line=None,
                    target_ratio=0.5,
                    straight_line_rate=0,
                    obstacle_rate=0,
                    name='DrawLines',
                    input_size=(250, 200)):
        """
        Arguments:
            xy0_range: A list of length-2 arrays.
                Every array is a coordinate [x, y].
                Every coordinate corresponds to the position of the lower
                intersection of the middle line.
            xy1_range: A list of length-2 arrays.
                Every array is a coordinate [x, y].
                Every coordinate corresponds to the position of the upper
                intersection of the middle line.
            radius_range: A list of > 0 integers.
                The middle line is in fact a circle.
                The bigger the radius, the straighter the line.
            thickness_range: A list of > 0 integers.
                The lines' thickness will be randomly drawn in the list.
            color_range: A `Colorange` object,
                containing all the RGB triplets of color.
            middle_line: triplet of int.
                plain = middle_line[0]
                empty = middle_line[1]
                line_type = middle_line[2]
            name: A string,
                the name of the layer so that it's easy to recognize it.
            input_size: 2-tuple of int,
                the size of the input image (width, height)
        """

        super(DrawLines, self).__init__()

        width_begin, height_begin = input_size

        if xy0_range is None:
            xy0_range = [[x, height_begin] for x in range(0, width_begin+1)]
        if xy1_range is None:
            xy1_range = [[0, y] for y in range(int(height_begin/2), 0, -1)]
            xy1_range += [[x, 0] for x in range(0, width_begin+1)]
            xy1_range += [[width_begin-1, y] for y in range(0, int(height_begin/2))]

        if radius_range is None:
            radius_range = list(range(200, 500)) + list(range(5000, 5300))
        if thickness_range is None:
            thickness_range = [6, 7, 8, 9, 10]
        if color_range is None:
            color_range = White() + Yellow()

        self.xy0_range = xy0_range
        self.xy1_range = xy1_range
        self.radius_range = radius_range
        self.thickness_range = thickness_range
        self.color_range = color_range

        self.input_size = input_size
        self.width = self.input_size[0]
        self.height = self.input_size[1]
        self.straight_line_rate = straight_line_rate
        self.obstacle_rate = obstacle_rate

        self.target_ratio = target_ratio

        self.obstacle_color_ranges = obstacle_color_ranges

        # Is there a VISIBLE middle line ? (the middle line always exists)
        # TODO: quite complex to have a 3-tuple for middle_line...
        if middle_line is not None:
            self.middle_line_plain = middle_line[0]
            self.middle_line_empty = middle_line[1]
            self.middle_line_type = middle_line[2]
            self.middle_line_color_range = middle_line[3]
        else:
            # Make it invisible by default
            self.middle_line_plain = None
            self.middle_line_empty = None
            self.middle_line_type = None
            self.middle_line_color_range = color_range

        self.max_width = 300
        self.name = name

    def call(self, im):

        if im is None:
            raise ValueError('img is None')

        img = im.copy()

        if self.straight_line_rate > random():
            img, angle, gas = self.draw_straight_line(img)
        else:
            # Current position of the car (the car is generally in the middle of
            # the lower bound of the image)
            pose = Point(self.width/2, self.height)

            # Middle line
            midline = self.generate_middle_line(self.xy0_range,
                                                self.xy1_range,
                                                self.radius_range,
                                                self.thickness_range,
                                                self.middle_line_color_range)

            # TODO: change this so that the distance between the 2 lines can be chosen
            # by the user
            # 200: harcoded value
            # 100: harcoded value
            width = randint(max(200, 2 * midline.x0 - self.width), self.max_width)

            # Draw all the visible lines
            img = self.draw_lines(img, midline, width=width, right_turn=True,
                                        color_range=self.color_range)

            # Get the angle and gas depending on the position of
            # the car with respect to the middle line.
            angle, gas, img = self.dir_gas(midline, pose, img, width)

        return img, angle, gas

    def dir_gas(self, curr_line, pose, img, road_width):
        """
        Calculates the (dir, gas) values given the position
        of the car compared to the middle line.

        Arguments:
            curr_line: A `RoadLine` object, the middle line.
            pose: A `Point` object, indicates the position of the car on the image.

        Returns:
            A couple (angle, gas), the angle of the car given its position
            compared to the middle line and the gas value.
            For now, the gas value is constant.
        """

        radius = curr_line.radius

        pt0 = Point(curr_line.x0, curr_line.y0)
        pt1 = Point(curr_line.x1, curr_line.y1)
            
        center = self.pts2center(pt0, pt1, radius)
        vect = self.target_ratio * (pt0 + pt1) - center
            
        target_pt = center + vect * (radius/vect.norm())
        target_vect = target_pt - pose
            
        angle = atan2(target_vect.x, -target_vect.y) * 6 / pi

        if random() < self.obstacle_rate:
            img, angle = self.add_obstacle(img, angle, target_vect, curr_line, pose)
            
        gas = 0.5

        return angle, gas, img

    def add_obstacle(self, img, angle, target_vect, curr_line, pose):
        draw = ImageDraw.Draw(img)
        width, height = 20 + randint(0, 20), 20 + randint(0, 20)
        x0, y0 = randint(0, 250 - width // 2), randint(0,  20 - height // 2)
        x1, y1 = x0 + width, y0 + height

        color_range = choice(self.obstacle_color_ranges)
        c = choice(color_range.colors)

        draw.rectangle((x0, y0, x1, y1), fill=c, outline=c)

        if curr_line.x0 >= pose.x:
            angle_left = atan2(x0, -y0) * 6 / pi
            angle_right = atan2(x1, -y1) * 6 / pi
        else:
            angle_left = atan2(x0, -y1) * 6 / pi
            angle_right = atan2(x1, -y0) * 6 / pi

        if angle_left <= angle <= angle_right:
            if curr_line.x0 >= x0:
                target_vect.x += np.abs(width / 2 - x0) / 2
            else:
                target_vect.x -= np.abs(width / 2 - x0) / 2

            angle = atan2(target_vect.x, -target_vect.y) * 6 / pi

        return img, angle

    def generate_middle_line(self, xy0_range, xy1_range, radius_range, thickness_range, color_range):
        """Creates the middle line of the road. The middle line position,
        thickness, radius and color is randomly drawn from the different
        range arguments.

        Arguments:
            xy0_range: A list of length-2 arrays.
                Every array is a coordinate [x, y].
                Every coordinate corresponds to the position of the lower
                intersection of the middle line.
            xy1_range: A list of length-2 arrays.
                Every array is a coordinate [x, y].
                Every coordinate corresponds to the position of the upper
                intersection of the middle line.
            radius_range: A list of > 0 integers.
                The middle line is in fact a circle.
                The bigger the radius, the straighter the line.
            thickness_range: A list of > 0 integers.
                The lines' thickness will be randomly drawn in the list.
            color_range: list of `Color` objects # TODO

        Returns:
            A `RoadLine` object
        """

        # A RoadLine is constituted of 2 points, (x0, y0) and (x1, y1)

        # First, let's choose the (x0, y0) one.
        index = int(gauss(len(xy0_range)//2, 50))
        while index >= len(xy0_range) or index < 0:
            index = int(gauss(len(xy0_range)//2, 50))
        x0, y0 = xy0_range[index]

        while 2 * x0 - self.width > self.max_width:
            index = int(gauss(len(xy0_range)//2, 50))
            while index >= len(xy0_range) or index < 0:
                index = int(gauss(len(xy0_range)//2, 50))
            x0, y0 = xy0_range[index]

        # Secondly, let's choose the (x1, y1) one.
        index = int(gauss(len(xy1_range)//2, 100))
        while index >= len(xy1_range) or index < 0:
            index = int(gauss(len(xy1_range)//2, 100))
        x1, y1 = xy1_range[index]

        # The bigger the radius, the straighter the line.
        radius = radius_range[randint(0, len(radius_range)-1)]
        thickness = thickness_range[randint(0, len(thickness_range)-1)]
        color = color_range.colors[randint(0, len(color_range.colors)-1)]

        return RoadLine(x0, y0, x1, y1, radius, thickness=thickness, color=color)

    def draw_lines(self, img, line, width=55, right_turn=True, color_range=None):
        """Draws the visible lines on the image.

        Arguments:
            img: A `PIL.Image` object,
                the image to modify.
            line: A `RoadLine` object,
                the middle line.
            width: > 0 integer,
                the distance between the 2 outer lines.
            right_turn: A Boolean,
                does the road goes to the right ?
                If `False`, goes to the left by symmetry.
            color_range: A `ColorRange` object,
                the different RGB values the line can take.

        Returns:
            The modified image.
        """

        # Real lines
        line1 = line.copy()
        line2 = line.copy()
        middle_line = line.copy()

        line1.color = choice(color_range.colors)
        line2.color = choice(color_range.colors)
        middle_line.color = choice(self.middle_line_color_range.colors)

        draw = ImageDraw.Draw(img)

        # Draw the outer lines
        self.draw_one_line(draw, line1 - int(width/2), right_turn=right_turn)
        self.draw_one_line(draw, line2 + int(width/2), right_turn=right_turn)

        # Draw the middle line if visible, depending on the type
        if self.middle_line_type == 'dashed':
            self.draw_one_line(draw, middle_line, right_turn=right_turn,
                          plain=self.middle_line_plain,
                          empty=self.middle_line_empty)
        elif self.middle_line_type == 'plain':
            self.draw_one_line(draw, middle_line, right_turn=right_turn)

        # Noise lines
        # TODO: these lines should be of a different color (like shadows...)
        if randint(0, 1):
            line1 = line.copy()
            line2 = line.copy()
            line1.color = choice(color_range.colors)
            line2.color = choice(color_range.colors)

            width_noise = (1.4 + 3 * random()) * width

            self.draw_one_line(draw, line1 - int(width_noise/2), right_turn=right_turn)
            self.draw_one_line(draw, line2 + int(width_noise/2), right_turn=right_turn)

        return img

    def draw_circle(self, draw, circle):
        """Draws a circle on a `ImageDraw` object.

        Arguments:
            draw: A `PIL.Draw` object.

            circle: A `Circle` object.

        """

        thickness = circle.thickness
        color = circle.color

        x0 = circle.center.x - circle.radius
        y0 = circle.center.y - circle.radius
        x1 = circle.center.x + circle.radius
        y1 = circle.center.y + circle.radius

        start = 0
        end = 360

        if circle.empty == 0:
            for i in range(0, thickness):
                diff = i - int(thickness/2)
                xy = [x0+diff, y0, x1+diff, y1]
                draw.arc(xy, start, end, fill=color)
        else:
            plain_angle = float(circle.plain)/circle.radius
            empty_angle = float(circle.empty)/circle.radius
            for i in range(0,thickness):
                diff = i - int(thickness/2)
                xy = [x0+diff, y0, x1+diff, y1]
                for angle in range(0, int(2*pi/(plain_angle+empty_angle))):
                    start = angle * (plain_angle+empty_angle)
                    end = start + plain_angle
                    draw.arc(xy, start*(180/pi), end*(180/pi), fill=color)

    def pts2center(self, pt1, pt2, radius, right_turn=True):
        """To draw a circle given 2 points and a radius, we need the center
        of the circle. We calculate it here.

        Arguments:
            pt1: A `Point` object,
                the first point belonging to the circle.
            pt2: A `Point` object,
                the second point belonging to the circle.
            radius: An integer,
                the radius of the circle.
            right_turn: A Boolean,
                does the road goes to the right ?
                If `False`, goes to the left by symmetry.

        Returns:
            A `Point` object modelizing the center of the circle.
        """

        vect = pt2 - pt1
        vect_orthog = Point(-vect.y, vect.x)

        vect_orthog = vect_orthog * (1/vect_orthog.norm())
        middle = (pt1 + pt2) * 0.5

        triangle_height = sqrt(radius*radius - (vect.norm() * 0.5 * vect.norm() * 0.5 ))
        center = middle + vect_orthog * triangle_height

        # Make sure the center is on the correct side of the points
        symmetry = True
        if center.x > middle.x:
            symmetry = False
        if not right_turn:
            symmetry = not symmetry

        # If not, take the symmetric point with respect to the middle
        if symmetry:
            center = 2 * middle - center

        return center

    
    def draw_straight_line(self, img):
        draw = ImageDraw.Draw(img)
        thickness = choice(self.thickness_range)

        offset = randint(0, 50)

        lines_color = choice(self.color_range.colors)
        draw.line((25 + offset, 0, 25 + offset, 200), width=thickness, fill=lines_color) 
        draw.line((225 - offset, 0, 225 - offset, 200), width=thickness, fill=lines_color) 

        nb_lines = 500 // (self.middle_line_plain + self.middle_line_empty)
        point = randint(0, self.middle_line_plain)
        middle_color = choice(self.middle_line_color_range.colors)
        for _ in range(nb_lines):
            draw.line((125, point, 125, point + self.middle_line_plain),
                      width=thickness, 
                      fill=middle_color)
            point += self.middle_line_plain
            point += self.middle_line_empty

        return img, 0.0, 0.5

    def draw_one_line(self, draw, line, right_turn=True, plain=1, empty=0):
        """Draws a line on the image.
        The method used to draw a line depends o the radius of the line,
        and if the line is dashed or not.

        Arguments:
            draw: A `PIL.ImageDraw` object,
                represents the image on which the lines
                are drawn.
            line: A `RoadLine` object,
                the line to draw.
            right_turn: A Boolean,
                does the road goes to the right ?
                If `False`, goes to the left by symmetry.
            plain: An integer,
                tells the proportion of 'plain' line.
                If empty is 0, the line is 'plain'.
            empty: An integer,
                tells the proportion of 'empty' line.
                If 0, the line is 'plain'. If not, the line is dashed.

        Returns:
            img: A `PIL.Image` object,
                the modified image.
            angle: A float,
                the angle to get to the right position considering
                the current picture, the position of the car, and the
                position of the middle line.
            gas: A float,
                the gas value.
        """

        if line.y1 > line.y0:
            x0, y0 = line.x1, line.y1
            x1, y1 = line.x0, line.y0
        else:
            x0, y0 = line.x0, line.y0
            x1, y1 = line.x1, line.y1

        if x0 == x1:
            # Straight line
            draw.line([x0, y0, x1, y1], fill=line.color, width=line.thickness)
        else:
            radius = line.radius
            pt0 = Point(x0, y0)
            pt1 = Point(x1, y1)
            center = self.pts2center(pt0, pt1, radius, right_turn=right_turn)
            thickness = line.thickness
            color = line.color

            circle1 = Circle(center, radius, thickness=thickness, color=color)

            # That is, the line is dashed
            if empty != 0:
                circle1.plain = plain
                circle1.empty = empty

            self.draw_circle(draw, circle1)

    def summary(self):
        """Returns a string describing this layer"""

        return '{}'.format(self.name)
