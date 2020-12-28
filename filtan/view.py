import sys
from pathlib import Path
import PySimpleGUI as sg
from gmail import Gmail


def required_files_exists(token_dir, token_paths):
    if not token_dir.is_dir():
        sg.Popup(
            'Caution',
            '「{}」フォルダが見つかりません。\nアプリケーションを終了します。'.format(token_dir.name)
        )
        return False
    elif not token_paths['pickle_path'].exists() and not token_paths['json_path'].exists():
        sg.Popup(
            'Caution',
            '{pickle_path}\n''または\n''{json_path}\nが見つかりません。\n''アプリケーションを終了します。'
            .format(**token_paths)
        )
        return False
    return True


def main():
    project_dir = Path(__file__).parents[1]
    token_dir = project_dir.joinpath('token')
    token_paths = {
        'pickle_path': token_dir.joinpath('token.pickle')
        , 'json_path': token_dir.joinpath('client_id.json')
    }
    # 必須ファイルなければ終了
    if not required_files_exists(token_dir, token_paths):
        sys.exit()

    g_mail = Gmail(token_paths)
    label_list = g_mail.label_list()
    labels = [label['name'] for label in label_list if label['type'] == 'user']

    filter_frame = [[
        sg.OptionMenu(['from', 'to', 'subject'], disabled=True, key='filter_type', size=(5, 1))
        , sg.InputText(disabled=True, key='filter_txt', default_text='', size=(20, 1))
    ]]
    layout = [
        [sg.Text('ラベル'), sg.Combo(labels, key='label', size=(25, 1))]
        , [sg.Checkbox('フィルターを作成する', key='is_filter', enable_events=True)]
        , [sg.Frame('フィルター', filter_frame, key='filter')]
        , [sg.Column([[sg.Button('作成', key='create', size=(6, 1))]], justification='right')]
    ]

    window = sg.Window('GMail Filter', layout, finalize=True, icon='icon/filtan.ico')

    while True:
        event, values = window.read()
        # ×ボタン押下(None)で閉じる
        if event is None:
            break
        else:
            input_label = values['label']
            input_filter_type = values['filter_type']
            input_filter_txt = values['filter_txt']

        if event == 'is_filter':
            # フィルターチェックボックスでフィルター入力可・不可切り替え
            if values['is_filter'] is True:
                window['filter_type'].update(disabled=False)
                window['filter_txt'].update(disabled=False)
            else:
                window['filter_type'].update(disabled=True)
                window['filter_txt'].update('', disabled=True)
        elif event == 'create':
            # 作成ボタン押下禁止
            window['create'].update(disabled=True)
            success_msg = ''
            error_msg = 'ラベルを入力してください。\n' if input_label == '' else ''
            # チェックボックス.get() => True: 1, False: 0
            if window['is_filter'].get() == 1 and input_filter_txt == '':
                error_msg += 'フィルターを入力してください。'

            if error_msg != '':
                sg.Popup('Error', error_msg)
            else:
                # チェックボックス.get() => True: 1, False: 0
                if window['is_filter'].get() == 1:
                    # 入力したラベル名からラベルID取得
                    label_id = ''
                    for label in label_list:
                        if label['name'] == values['label']:
                            label_id = label['id']
                            break

                    # 既存のラベルじゃなければ作成
                    if label_id == '':
                        label_result = g_mail.create_label(input_label)
                        if type(label_result) is dict:
                            success_msg += 'ラベル「{}」の作成に成功しました。\n'.format(input_label)
                            # ラベルリスト更新
                            labels = [label['name'] for label in g_mail.label_list() if label['type'] == 'user']
                            window['label'].update(value=label_result['name'], values=labels)
                            # フィルター作成
                            filter_result = g_mail.create_filter(
                                input_filter_type,
                                input_filter_txt,
                                label_result['id']
                            )
                        else:
                            filter_result = None
                            error_msg += label_result
                    else:
                        filter_result = g_mail.create_filter(input_filter_type, input_filter_txt, label_id)

                    if type(filter_result) is dict:
                        success_msg += 'フィルター「{}:{}」の作成に成功しました。\n'.format(input_filter_type, input_filter_txt)
                    else:
                        error_msg += filter_result
                else:
                    if input_label in labels:
                        error_msg += 'そのラベル名はすでにあります。\n別の名前を付けてください。'
                    else:
                        label_result = g_mail.create_label(input_label)
                        if label_result['name'] == values['label']:
                            success_msg = 'ラベル「{}」の作成に成功しました。'.format(label_result['name'])
                            labels = [label['name'] for label in g_mail.label_list() if label['type'] == 'user']
                            window['label'].update(value=label_result['name'], values=labels)
                # ポップアップ表示
                if success_msg:
                    sg.Popup('Success', success_msg)
                elif error_msg:
                    sg.Popup('Error', error_msg)
        # ボタン押下禁止解除
        window['create'].update(disabled=False)

    window.close()


if __name__ == '__main__':
    main()
