
class InjectionError(Exception):
    def __init__(self,reason,data=None,anomaly_type=None):
        self.data = data
        self.reason = reason
        if data is None:
            message = f"Error injecting errors: {reason}" +\
                      (f" for {anomaly_type} anomaly" if anomaly_type is not None else "")
        else:
            message = f"Error injecting errors into {data} data: {reason}" +\
                      (f" for {anomaly_type} anomaly" if anomaly_type is not None else "")
        super().__init__(message)

