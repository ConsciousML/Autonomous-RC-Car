from sklearn import metrics

def get_confusion_matrix(y_test, y_pred):
    print(metrics.confusion_matrix(y_test, y_pred))
    ff, fl, fr, lf, ll, lr, rf, rl, rr = metrics.confusion_matrix(y_test, y_pred).ravel()
    n = len(y_test)
    print("FF: %04d FL: %04d FR: %04d" % (ff, fl, fr))
    print("LF: %04d LL: %04d LR: %04d" % (lf, ll, lr))
    print("RF: %04d RL: %04d RR: %04d\n" % (rf, rl, rr))
    print(metrics.classification_report(y_test, y_pred, target_names=["forward", "left", "right"]))
    acc = (ff + ll + rr) / n
    print("Accuracy: %f" % acc)
    return ff, fl, fr, lf, ll, lr, rf, rl, rr