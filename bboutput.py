import datetime
import os
import subprocess


def log(name, participant_name, data):
    file_name = str.join('_', [name, participant_name, 'utc',
                               str(datetime.datetime.utcnow()).replace(' ', '_').replace(':', '')]) + '.txt'
    data.insert(0, file_name)
    with open(file_name, 'w') as f:
        f.write('\n'.join(map(str, data)))


def praat_play(mode, pms, vtl, df, prf):
    path = os.getcwd() + '\Praat.exe'
    subprocess.call([path,
                    '--run', 'manipulateSound.praat',
                     '{0}'.format(mode + '.wav'),
                     '{0}'.format(pms),
                     '{0}'.format(vtl),
                     '{0}'.format(df),
                     '{0}'.format(prf)])
