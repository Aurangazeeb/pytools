import os
import datetime as dt

file_delim = '__'
file_datestamp_style = '%a_%d_%b_%Y'
file_timestamp_style = '%H_%M_%S'

def manage_file(
    file_parent, 
    file_stem, 
    outputfile_ext, 
    add_time=True, 
    categorize_by_day=True):
        '''
        Creates file root if does not exist and append the filename prefix with it.
        Generates Day based directories and timebased files.
        By default generates a directory structure as follows:
            - prefix dir
                - current day dir
                    - filename_head with timestamp

        '''

        # associate file name with time
        if add_time:
            time_now = dt.datetime.now().strftime("%X").replace(':', '_')
            filename = f'{file_stem}{file_delim}{time_now}{outputfile_ext}'
        else:
            filename = f'{file_stem}{outputfile_ext}'

        # if want to categorize files based on daystamp
        if categorize_by_day:
            todays_datestamp = dt.datetime.now().strftime(file_datestamp_style)  # day num, mini day name, mini month name, full year
            # day based file directory naming
            file_parent = os.path.join(file_parent, todays_datestamp)
        # make the search dir if not exists
        if not os.path.exists(file_parent):
            os.makedirs(file_parent)
        filename = os.path.join(file_parent, filename)
        return filename