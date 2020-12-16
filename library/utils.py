class Utils():
    """Class for Utils"""

    # INITIALIZE
    def __init__(self):
        """The Constructor for Utils class"""
        super(Utils, self).__init__()

    def data_log(self, data='', divider=False):
        """ DATA LOG """

        with open('/home/admin/miscea-backend/logs.txt',"a+") as output_file:

            div = "*"*100

            if divider:

                output_file.write('{0}\n'.format(div))

            else:

                output_file.write('{0}\n'.format(data))

        return 1
