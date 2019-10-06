# Workspace_pathlib object, app_settings


class CommonUtils:



    @staticmethod
    def safe_cast(val, to_type, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default