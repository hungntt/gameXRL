import argparse
import base64
import io

from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def main_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--app_type', help='Flask app run type: remote (to connect from your own device to IRender)'
                                           'or server (only for running web on IRender) (default: server)',
                        type=str, default='server')
    parser.add_argument('--cnx_type', help='Database: local (database on your own device) '
                                           'or server (only for running web on IRender) '
                                           'or remote (to connect from your own device to IRender)'
                                           '(default: server)',
                        type=str, default='server')

    return parser.parse_args()


def plot_png(image):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(image)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(output.getvalue()).decode('utf8')

    return pngImageB64String
