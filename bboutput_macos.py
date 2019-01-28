import datetime
import os
import subprocess


def log(path, name, participant_name, data):
    file_name = str.join('_', [name, participant_name, 'utc',
                               str(datetime.datetime.utcnow()).replace(' ', '_').replace(':', '')]) + '.txt'
    data.insert(0, file_name)
    with open(path + '/' + file_name, 'w') as f:
        f.write('\n'.join(map(str, data)))


def praat_play(path, mode, pms, vtl, df, prf):
    praat = '/Praat.app/Contents/MacOS/Praat'
    sound = '/' + mode + '.wav'
    script = '/manipulateSound.praat'
    path_praat, path_sound, path_script = path + praat, path + sound, path + script
    subprocess.call([path_praat,
                    '--run', path_script,
                     '{0}'.format(path_sound),
                     '{0}'.format(pms),
                     '{0}'.format(vtl),
                     '{0}'.format(df),
                     '{0}'.format(prf)])