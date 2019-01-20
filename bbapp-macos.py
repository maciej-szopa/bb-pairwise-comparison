import bbdata
import bbprocess
import copy
import bboutput
from tkinter import *
from random import shuffle

pms_range, vtl_range, df_range, prf_range = [-10.0, 10.0], [0.6, 1.4], [0.6, 1.4], [0.1, 10]
ranges = [pms_range, vtl_range, df_range, prf_range]
current_path = sys.argv[1]


class WelcomeWindow:
    def __init__(self, master):
        def __init__(self, master):
            self.agreed = IntVar()
            understand_str = '\nConsent'
            psa_str = '\nExperiment code and personnel'
            welcome_str = '=============================  Your task  =============================\n\n' \
                          'In each trial, you will be played two recordings of the sentence \'I owe you a yoyo\'.\n' \
                          'You will be also given a description of an emotion.\n' \
                          'Imagine that sentence pronounced with this emotion.\n' \
                          'Out of the two sounds played, choose the sound \n' \
                          'that is closer to the emotional prototype that you imagined.\n\n' \
                          'Estimated duration: 30 minutes. You have to complete the experiment in one sitting.\n' \
                          'Roughly in the middle there will be quick break.\n' \
                          'You will start with a quick test run to adjust your playback volume.\n\n' \
                          '==================================================================\n\n' \
                          'Please enter your details below, tick the box and click the button to start the test run.\n'

            self.psa_label = Label(master, text=psa_str, fg='red')
            self.psa_label.pack()
            self.welcome_label = Label(master, text=welcome_str)
            self.welcome_label.pack()
            self.name_label = Label(master, text='Name (no special characters):')
            self.name_label.pack()
            self.input_name = Entry(master)
            self.input_name.pack()
            self.details_label = Label(master, text='Email:')
            self.details_label.pack()
            self.input_details = Entry(master)
            self.input_details.pack()
            self.agree_checkbutton = Checkbutton(master, text=understand_str, font=('default', 7), variable=self.agreed)
            self.agree_checkbutton.pack()
            self.go = Button(master, text='Start experiment', fg='green', command=lambda: self.open_window(master))
            self.go.pack()

    def open_window(self, master):
        if self.input_name.get() != '' and self.input_details.get() != '' and self.agreed.get() == 1:
            app = App(master, self.input_name.get(), self.input_details.get())


class App:

    def __init__(self, master, input_name, input_details):
        self.log, self.winners = [input_name, input_details], []
        self.current_filename = ''
        self.modes = ['yoyo_breathy4', 'yoyo_modal', 'yoyo_pressed3']
        self.euclid_left, self.euclid_right, self.euclid_avg, self.euclid = [], [], [], []
        self.playing_left, self.playing_mid, self.playing_right = StringVar(), StringVar(), StringVar()
        self.current_emotion = StringVar()
        self.current_button = IntVar()

        self.window = Toplevel(master)
        self.window.title('Experiment Window')

        self.display_emotion = Label(self.window, textvariable=self.current_emotion)
        self.display_emotion.grid(row=0, column=1)
        self.label_task = Label(self.window, text='\nWhich sound is closer\nto your prototype?')
        self.label_task.grid(row=1, column=1)

        self.label_left = Label(self.window, textvariable=self.playing_left)
        self.label_left.grid(row=2, column=0)
        self.label_mid = Label(self.window, textvariable=self.playing_mid)
        self.label_mid.grid(row=2, column=1)
        self.label_right = Label(self.window, textvariable=self.playing_right)
        self.label_right.grid(row=2, column=2)
        self.sound_left = Button(self.window, text='FIRST', fg='green', padx=30, pady=30,
                                 command=lambda: self.update_best_guess(self.euclid_left, 0))
        self.sound_left.grid(row=3, column=0)
        self.sound_average = Button(self.window, text='both are\nequally close', fg='green', padx=15, pady=15,
                                    command=lambda: self.update_best_guess(self.euclid_avg, 2))
        self.sound_average.grid(row=3, column=1)
        self.sound_right = Button(self.window, text='SECOND', fg='green', padx=30, pady=30,
                                  command=lambda: self.update_best_guess(self.euclid_right, 1))
        self.sound_right.grid(row=3, column=2)
        self.replay_both = Button(self.window, text='Replay', padx=30,
                                  command=self.play_choices)
        self.replay_both.grid(row=4, column=1)
        self.resume_button = Button(self.window, text='Resume', fg='blue', padx=30, pady=30,
                                    command=self.resume)
        self.feedback = Text(self.window)
        self.quit = Button(self.window, text='QUIT', fg='red', command=lambda: close_app(self))
        self.quit.grid(row=7, column=1)

        self.sound_average.grid_remove()
        self.p1 = bbdata.Participant(input_name)
        self.window.update()
        self.full_trial(self.p1)

    # <editor-fold desc="Playback">
    def play_again(self, split, button):
        if button == 0:
            playing = self.playing_left
        elif button == 1:
            playing = self.playing_right
        else:
            playing = self.playing_mid
        # print(button)
        playing.set('PLAYING')
        # print(playing.get())
        self.window.update()
        bboutput.praat_play(current_path, self.current_filename, split[0], split[1], split[2], split[3])
        self.window.update()
        playing.set('')

    def play_choices(self):
        self.play_again(self.euclid_left, 0)
        self.window.after(300, lambda: self.play_again(self.euclid_right, 1))

    def play_voice_choices(self):
        self.current_filename = self.modes[0]
        self.play_again(self.euclid_left, 0)
        self.current_filename = self.modes[2]
        self.play_again(self.euclid_avg, 2)
        self.current_filename = self.modes[1]
        self.play_again(self.euclid_right, 1)

    def update_buttons(self, choice1, choice2, dim):
        choices = [choice1, choice2]
        for a in choices:
            a.winner = False
        self.euclid_left, self.euclid_right = choices[0].euclid, choices[1].euclid
        choices[0].button, choices[1].button = 0, 1
        self.euclid_avg = bbprocess.average(self.euclid_left, self.euclid_right, dim)

    def update_best_guess(self, value, button):
        value = [round(dim_value, 4) for dim_value in value]
        self.euclid = value
        self.current_button.set(button)
    # </editor-fold>

    def full_trial(self, participant):
        self.test_trial()
        self.emotion_trial(participant.happy)
        self.emotion_trial(participant.depressed)
        self.emotion_trial(participant.grief_stricken)
        self.take_a_break()
        self.emotion_trial(participant.scared)
        self.emotion_trial(participant.angry)
        self.voice_trial(participant)
        self.conclude()

    def test_trial(self):
        self.current_emotion.set('\n-----------\nThe emotion name \nwill be displayed here\n-----------\n'
                                 '\nAdjust your playback volume and ensure you can hear the sounds.\n'
                                 'When you are ready, press one of the green buttons to start the experiment.')
        self.current_filename = 'yoyo_modal'
        self.euclid_left, self.euclid_right = [1, 1.1, 1.2, 1.2], [0.5, 1.2, 1.1, 1.1]
        self.window.after(500, lambda: self.play_choices())
        self.sound_left.wait_variable(self.current_button)
        self.euclid_left, self.euclid_right = [], []
        self.current_button.set(-1)

    # <editor-fold desc="Acoustic trial">
    def emotion_trial(self, emotion):
        self.current_filename = emotion.prototype[0]
        self.current_emotion.set('\n-----------\nCurrent emotion:\n{}\n-----------\n'.format(emotion.name))
        self.window.update()
        self.window.lift()

        self.euclid = emotion.prototype[1:]
        neutral = emotion.prototype[1:]
        self.log.append(emotion.name)
        pms1 = self.first_pass(0, neutral)
        vtl1 = self.first_pass(1, self.euclid)
        df1 = self.first_pass(2, self.euclid)
        prf1 = self.first_pass(3, self.euclid)
        pms2 = self.a_pass(0, 2, pms1, self.euclid)
        vtl2 = self.a_pass(1, 2, vtl1, self.euclid)
        df2 = self.a_pass(2, 2, df1, self.euclid)
        prf2 = self.a_pass(3, 2, prf1, self.euclid)
        pms3 = self.a_pass(0, 3, pms2, self.euclid)
        vtl3 = self.a_pass(1, 3, vtl2, self.euclid)
        df3 = self.a_pass(2, 3, df2, self.euclid)
        prf3 = self.a_pass(3, 3, prf2, self.euclid)
        pms4 = self.a_pass(0, 4, pms3, self.euclid)
        vtl4 = self.a_pass(1, 4, vtl3, self.euclid)
        df4 = self.a_pass(2, 4, df3, self.euclid)
        prf4 = self.a_pass(3, 4, prf3, self.euclid)
        pms5 = self.a_pass(0, 5, pms4, self.euclid)
        # vtl5 = self.a_pass(1, 5, vtl4, self.euclid)
        # df5 = self.a_pass(2, 5, df4, self.euclid)
        prf5 = self.a_pass(3, 5, prf4, self.euclid)

        emotion.prototype = [self.current_filename] + prf5.get_winner().euclid
        self.log.append('WINNER: ' + str(emotion.prototype) + '\n\n')
        self.winners.append(str(emotion.prototype[1:]))

    def first_pass(self, dim, emotion):
        message = '\npass {}, dimension {}'
        self.log.append(message.format(1, dim))

        ans = bbdata.Answer()
        the_range = ranges[dim]
        ans.a.val = the_range[0] + 0.5 * (the_range[1] - the_range[0])
        # print('a value:', ans.a.val)
        ans.a1.euclid, ans.a.euclid, ans.a2.euclid = bbprocess.set_choices(ans.a.val, ranges, dim, 1, emotion)
        # print('Choices:', ans.a1.euclid, ans.a.euclid, ans.a2.euclid)
        self.log.append('Stage 1 Choices: ' + str([ans.a1.euclid, ans.a2.euclid]))
        self.update_buttons(ans.a1, ans.a2, dim)
        self.window.after(500, lambda: self.play_choices())
        self.sound_left.wait_variable(self.current_button)
        self.log.append('Button pressed: ' + str(self.current_button.get()))

        ans.stage2 = list(map(copy.copy, [ans.set_winner(self.current_button.get(), 0), ans.a]))
        # print('Stage 1 winner:', ans.get_winner().euclid)
        self.log.append('Stage 1 winner: ' + str(ans.get_winner().euclid[dim]))
        ans.stage2.sort(key=lambda x: x.euclid[dim])
        # print('Stage 2 choices:', [a.euclid for a in ans.stage2])
        self.log.append('Stage 2 choices:' + str([a.euclid for a in ans.stage2]))
        self.update_buttons(ans.stage2[0], ans.stage2[1], dim)
        self.play_choices()
        self.sound_average.grid()
        self.sound_left.wait_variable(self.current_button)
        self.log.append('Button pressed: ' + str(self.current_button.get()))
        if self.current_button.get() == 2:
            avg_choice = bbdata.Choice()
            avg_choice.euclid = self.euclid_avg
            avg_choice.button = 2
            ans.stage2.append(avg_choice)
        self.sound_average.grid_remove()
        ans.set_winner(self.current_button.get(), 1)
        # print('Done. Current euclid:', self.euclid, 'Winner euclid:', ans.get_winner().euclid)
        self.log.append('Stage 2 winner: ' + str(ans.get_winner().euclid[dim]))

        return ans

    def a_pass(self, dim, passno, ans, emotion):
        message = '\npass {}, dimension {}'
        self.log.append(message.format(passno, dim))

        direction1 = ans.get_direction(ans.get_winner(), dim)
        ans2 = bbdata.Answer()
        ans2.a.val = self.euclid[dim]
        # print('a value:', ans2.a.val)
        ans2.a1.euclid, ans2.a.euclid, ans2.a2.euclid = bbprocess.set_choices(ans2.a.val, ranges, dim, passno, emotion)
        # print('Choices:', ans2.a1.euclid, ans2.a.euclid, ans2.a2.euclid)
        if ans2.a1.euclid == ans2.a.euclid:
            stage1 = [ans2.a, ans2.a2]
        elif ans2.a.euclid == ans2.a2.euclid:
            stage1 = [ans2.a1, ans2.a]
        else:
            stage1 = [ans2.a1, ans2.a] if direction1 == 0 else [ans2.a, ans2.a2]
        self.log.append('Stage 1 choices: ' + str([a.euclid for a in stage1]))
        # print('Stage 1 choices:', [a.euclid for a in stage1], 'direction:', direction1)
        self.update_buttons(stage1[0], stage1[1], dim)
        self.play_choices()
        self.sound_left.wait_variable(self.current_button)
        self.log.append('Button pressed: ' + str(self.current_button.get()))
        ans2.set_winner(self.current_button.get(), 0)
        # print('Stage 1 winner:', ans2.get_winner().euclid)
        self.log.append('Stage 1 winner: ' + str(ans2.get_winner().euclid[dim]))

        if ans2.a.winner and ans2.a1.euclid != ans2.a.euclid and ans2.a.euclid != ans2.a2.euclid:
            if direction1 == -1:
                second_choice = ans2.a2 if ans.a.euclid == ans2.a1.euclid else ans.a1
            else:
                second_choice = ans2.a1 if direction1 == 1 else ans2.a2
            ans2.stage2 = list(map(copy.copy, [ans2.a, second_choice]))
            ans2.stage2.sort(key=lambda x: x.euclid[dim])
            # print('Stage 2 choices:', [a.euclid for a in ans2.stage2])
            self.log.append('Stage 2 choices: ' + str([a.euclid for a in ans2.stage2]))
            self.update_buttons(ans2.stage2[0], ans2.stage2[1], dim)
            self.play_choices()
            self.sound_average.grid()
            self.sound_left.wait_variable(self.current_button)
            self.log.append('Button pressed: ' + str(self.current_button.get()))
            if self.current_button.get() == 2:
                avg_choice = bbdata.Choice()
                avg_choice.euclid = self.euclid_avg
                avg_choice.button = 2
                ans2.stage2.append(avg_choice)
            self.sound_average.grid_remove()
            ans2.set_winner(self.current_button.get(), 1)
            self.log.append('Stage 2 winner: ' + str(ans2.get_winner().euclid[dim]))
        # print('Done. Current euclid:', self.euclid, 'Winner euclid:', ans2.get_winner().euclid)
        return ans2

    def take_a_break(self):
        self.label_task.grid_remove()
        self.sound_left.grid_remove()
        self.sound_right.grid_remove()
        self.replay_both.grid_remove()
        self.resume_button.grid(row=5, column=1)
        self.current_emotion.set('You are halfway done.\n'
                                 'Feel free to take a short break.\n'
                                 'When you are ready to return, press the Resume button.')
        self.log.append('----------Break---------')
        self.resume_button.wait_visibility(self.label_task)

    def resume(self):
        self.resume_button.grid_remove()
        self.label_task.grid()
        self.sound_left.grid()
        self.sound_right.grid()
        self.replay_both.grid()
        self.window.update()
    # </editor-fold>

    def voice_trial(self, participant):
        self.sound_average.grid()
        self.sound_left.configure(command=lambda: self.current_button.set(0))
        self.sound_average.configure(text='SECOND', command=lambda: self.current_button.set(2))
        self.sound_right.configure(text='THIRD', command=lambda: self.current_button.set(1))
        self.replay_both.configure(command=self.play_voice_choices)
        self.voice_pass(participant.happy)
        self.voice_pass(participant.depressed)
        self.voice_pass(participant.grief_stricken)
        self.voice_pass(participant.scared)
        self.voice_pass(participant.angry)

    def voice_pass(self, emotion):
        self.current_emotion.set('\n-----------\nCurrent emotion:\n{}\n-----------\n'.format(emotion.name))
        shuffle(self.modes)
        sliced = emotion.prototype[1:]
        self.euclid_left, self.euclid_avg, self.euclid_right = sliced, sliced, sliced
        self.play_voice_choices()
        self.sound_left.wait_variable(self.current_button)
        for i, mode in enumerate(self.modes):
            if i == self.current_button.get():
                self.winners.append(mode)
                self.log.append(emotion.name + ': ' + mode)

    def conclude(self):
        self.label_task.grid_remove()
        self.sound_left.grid_remove()
        self.sound_average.grid_remove()
        self.sound_right.grid_remove()
        self.replay_both.grid_remove()
        self.quit.configure(text='Submit & Exit', fg='green', command=lambda: submit_and_close(self))
        self.current_emotion.set('\nThank you for participating!\n'
                                 'If you have any feedback, you can enter it below.\n'
                                 'Click QUIT to finish the experiment.\n')
        self.feedback.grid(row=5, column=1)


def close_app(app):
    app.log = app.winners + ['\n\n'] + app.log
    app.log.append('\n--------Session terminated by user--------')
    output.log(current_path, 'results_bb', app.p1.name, app.log)
    root.destroy()


def submit_and_close(app):
    app.log.append('Feedback:')
    app.log.append(app.feedback.get('1.0', END))
    close_app(app)

root = Tk()
root.title('Prototype approximation')
welcome = WelcomeWindow(root)
root.mainloop()