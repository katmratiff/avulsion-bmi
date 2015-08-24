#! /usr/bin/env python
import sys
import os
import shutil

import numpy as np


def plot_elevation(avulsion):
    import matplotlib.pyplot as plt

    z = avulsion.get_value('land_surface__elevation')

    plt.imshow(z, origin='lower', cmap='terrain')
    plt.colorbar().ax.set_label('Elevation (m)')
    plt.show()


def main():
    import argparse
    from avulsion_bmi import BmiRiverModule

    parser = argparse.ArgumentParser('Run the avulsion model')
    parser.add_argument('file', help='YAML-formatted parameters file')
    parser.add_argument('--days', type=int, default=0,
                        help='Run model for DAYS')
    parser.add_argument('--years', type=int, default=0,
                        help='Run model for YEARS')
    parser.add_argument('--plot', action='store_true',
                        help='Plot final elevations')
    parser.add_argument('--save', action='store_true',
                        help='Save output files')
    parser.add_argument('--spacing', type=int, default=1,
                        help='Spacing for saved files (timesteps)')
    parser.add_argument('--runID', type=int, default=1,
                        help='Experiment ID number')

    args = parser.parse_args()

    np.random.seed(1945)

    avulsion = BmiRiverModule()
    avulsion.initialize(args.file)

    if args.save:
        os.mkdir("run" + str(args.runID))
        os.mkdir("run" + str(args.runID) + "/elev_grid" + str(args.runID))
        os.mkdir("run" + str(args.runID) + "/riv_course" + str(args.runID))
        shutil.copy(args.file, "run" + str(args.runID))
        #os.mkdir("run" + str(args.runID) + "/profile")

    n_steps = int((args.days + args.years * 365.) / avulsion.get_time_step())
    for k in xrange(n_steps):
        avulsion.update()

        if args.save & (k % args.spacing == 0):
            z = avulsion.get_value('land_surface__elevation')
            x = avulsion.get_value('channel_centerline__x_coordinate')
            y = avulsion.get_value('channel_centerline__y_coordinate')
            #prof = z[x, y]

            np.savetxt('run' + str(args.runID) + '/elev_grid' + str(args.runID) + '/elev_'
                       + str(k*avulsion.get_time_step()) + '.out', z, fmt='%.5f')
            np.savetxt('run' + str(args.runID) + '/riv_course' + str(args.runID) + '/riv_'
                       + str(k*avulsion.get_time_step()) + '.out', zip(x, y), fmt='%i')
            #np.savetxt('profile/prof_' + str(k) + '.out', prof, fmt='%.5f')

    if args.plot:
        plot_elevation(avulsion)

    #z = avulsion.get_value('land_surface__elevation')
    #np.savetxt(sys.stdout, z)

    avulsion.finalize()


if __name__ == '__main__':
    main()
