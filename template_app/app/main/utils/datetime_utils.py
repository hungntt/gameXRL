"""
Get date time for saving database and logging
"""

import datetime


def get_current():
    """Get date time current of system
    Returns:
        {datetime} -- date time current with format y-m-d h:m:s
    """
    create_date = datetime.datetime.now()
    create_date = create_date.strftime("%Y-%m-%d %H:%M:%S")
    return create_date


def get_current_upload():
    """Get date time current of system for uploading service
    Returns:
        {string} -- date time current with format ymd
    """
    create_date = datetime.datetime.now()
    create_date = create_date.strftime("%Y%m%d")
    return str(create_date)
