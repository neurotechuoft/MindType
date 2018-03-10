class FeatureFlags():
    """
        Feature toggling to allow for trunk-based development for features
        still in development. Turn on or off the features you want by setting
        the values to true or false.
    """
    DEV_TOOLS = False
    GUI = True
    COMMAND_LINE = False
    BOARD = True
    SERVER = True
    STREAM_RT = True
    ANALYSIS_RT = False
    LDA = False
