import sys
import os

class Controller():

    def __init__(self):
        self.list_argv = []
        self.arg_reader()
        self.manager()

    def arg_reader(self):
        if len(sys.argv) <= 1:
            self.list_argv = []
        else:
            self.list_argv = sys.argv[1:]

    def manager(self):
        if len(self.list_argv) == 0:
            display.usage_print()
        else:
            if self.list_argv[0] == '-h':
                display.usage_print()
            else:
                model.db_opener()
                if self.list_argv[0] == '-l':
                    display.list_printer()
                elif self.list_argv[0] == '-c':
                    model.db_checker(self.list_argv[1])
                    model.db_updater()
                    display.list_printer()
                elif self.list_argv[0] == '-a':
                    if len(self.list_argv) == 1:
                        display.error_add_remove()
                    else:
                        model.db_adder(' '.join(self.list_argv[1:]))
                        display.list_printer()
                elif self.list_argv[0] == '-e':
                    model.db_eraser()
                    display.list_eraser()
                elif self.list_argv[0] == '-r':
                    if len(self.list_argv) == 1:
                        display.error_add_remove()
                    else:
                        model.db_remover(self.list_argv[1])
                        model.db_updater()
                        display.list_printer()

                else:
                    display.error_argument()
                    display.usage_print()


class Model():

    def __init__(self):
        self.task_list = []

    def db_opener(self):
        self.file = open('db.txt', 'r+')
        self.task_list_raw = self.file.readlines()
        for task in self.task_list_raw:
            self.task_list.append(task.split('|||'))

    def db_adder(self, task_to_add):
        self.task_list.append(['0', str(task_to_add) + '\n'])
        self.file.write('0'+'|||'+str(task_to_add) + '\n')
        self.file.close()

    def db_eraser(self):
        self.eraser = input('Are you sure? (Y/N) ')
        if self.eraser == 'Y':
            self.file.close()
            self.file = open('db.txt', 'w')
            self.file.close()

    def db_checker(self, num):
        try:
            self.task_list[int(num)-1][0] = '1'
        except IndexError:
            display.error_index()
        except ValueError:
            display.error_value()

    def db_updater(self):
        self.file.close()
        self.file = open('db.txt', 'w')
        for i in range(len(self.task_list)):
            self.file.write(self.task_list[i][0] + '|||' + self.task_list[i][1])
        self.file.close()
        return self.task_list

    def db_remover(self, num):
        try:
            self.task_list.remove(self.task_list[int(num)-1])
        except IndexError:
            display.error_index()
        except ValueError:
            display.error_value()

class Display():

    def __init__(self):
        self.not_checked = '[ ] '
        self.checked = '[X] '

    def usage_print(self):
        print(' Python Todo application\n ======================= \n \n Command line arguments: \n')
        print(' -h   Help on command line arguments.')
        print(' -l   Lists all the tasks')
        print(' -a   Adds a new task')
        print(' -r   Removes a task. Enter task number.')
        print(' -c   Completes a task. Enter task number.')
        print(' -e   Empty task list')

    def list_printer(self):
        if model.task_list == []:
            print('No todos for today!')
        else:
            print('\nThings to do:')
            for i in range(len(model.task_list)):
                if model.task_list[i][0] == '0':
                    print(str(i+1) + ' - ' + self.not_checked + model.task_list[i][1][:-1])
                else:
                    print(str(i+1) + ' - ' + self.checked + model.task_list[i][1][:-1])

    def list_eraser(self):
        if model.eraser == 'Y':
            print('List successfully erased.')
        else:
            print('Exit without erasing.')

    def error_argument(self):
        print('\nUnsupported argument. \n')

    def error_add_remove(self):
        print('\nUnable to perform: no task provided. \n')

    def error_index(self):
        print('\nUnable to perform: index is out of bound. \n')

    def error_value(self):
        print('\nUnable to perform: index is not a number. \n')

display = Display()
model = Model()
controller = Controller()
