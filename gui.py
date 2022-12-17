import functions as fn
import PySimpleGUI as sg
import time

sg.theme("BLack")

clock = sg.Text('', key='clock')
label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo", key="todo")
add_button = sg.Button("Add")
list_box = sg.Listbox(values=fn.read_todos(), key='todos',
                      enable_events=True, size=[45, 10])
edit_button = sg.Button("Edit")
complete_button = sg.Button("complete")
exit_button = sg.Button("Exit")

window = sg.Window('My To-Do App',
                   layout=[[clock],
                           [label],
                           [input_box, add_button],
                           [list_box, edit_button, complete_button],
                           [exit_button]],
                   font=('Helvetica', 20))
while True:
    event, values = window.read(timeout=200)
    window["clock"].update(value=time.strftime("%b %d, %Y %H:%M:%S"))
    print(event)
    print(values)
    # print(values['todos'])
    match event:
            case "Add":
                try:
                    todos = fn.read_todos()
                    new_todo = values['todo'] + "\n"
                    todos.append(new_todo)
                    fn.write_todos(todos)
                    window['todos'].update(values=todos)
                except TypeError as err:
                    continue

            case "Edit":
                try:
                    todo_to_edit = values['todos'][0]
                    new_todo = values['todo']

                    todos = fn.read_todos()
                    index = todos.index(todo_to_edit)
                    todos[index] = new_todo
                    fn.write_todos(todos)

                    window['todos'].update(values=todos)
                except IndexError:
                    sg.popup("Please select an item first", font=("Helvetica", 20))

            case "complete":
                todo_to_complete = values['todos'][0]
                todos = fn.read_todos()
                todos.remove(todo_to_complete)
                fn.write_todos(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value='')

            case "Exit":
                break
            case 'todos':
                window['todo'].update(value=values['todos'][0])

            case sg.WIN_CLOSED:
                break

window.close()
