#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import json

from flask import Blueprint, redirect, request

from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, Form, InputText, InputButton
from app.adecty_design.interfaces import interface
from app.database.models import Admin, ArticleItem, Account
from app.database import Text as TextDB
from app.decorators.admin_get import admin_get


blueprint_chapter = Blueprint(
    name='blueprint_chapter',
    import_name=__name__,
    url_prefix='/<int:related_block_id>/'
)


@blueprint_chapter.route(rule='/deleted', endpoint='delete_chapter', methods=['GET', 'POST'])
@admin_get(not_return=True)
def delete_chapter(article_id: int, block_id: int, related_block_id: int):
    chapter = ArticleItem.get_or_none(ArticleItem.id == related_block_id)

    if chapter:
        chapter.delete_instance()

    return redirect(f'/articles/{article_id}/{block_id}')


@blueprint_chapter.route(rule='/edit', endpoint='chapter_edit', methods=['GET', 'POST'])
@admin_get()
def chapter_edit(admin: Admin, article_id: int, block_id: int, related_block_id: int):
    root_block = ArticleItem.get_or_none(ArticleItem.id == related_block_id)
    account = Account.get_by_id(admin.account_id)

    if request.method == 'POST':
        new_value = request.form.get('new_value')
        new_url = request.form.get('new_url')
        root_block_data = json.loads(root_block.data)
        if root_block_data:
            if 'text' in root_block_data:
                if new_value:
                    text_id = root_block_data['text']
                    if text_id:
                        text_id = TextDB.get_or_none(TextDB.id == text_id)
                        if text_id:
                            text_id.value_set(account, new_value)
                        else:
                            new_text = TextDB()
                            new_text.save()
                            new_text.default_create(value=new_value)
                            root_block_data['text'] = new_text.id
                    else:
                        new_text = TextDB()
                        new_text.save()
                        new_text.default_create(value=new_value)
                        root_block_data['text'] = new_text.id
                else:
                    root_block_data.pop('text', None)
            if 'url' in root_block_data:
                if new_url:
                    url_id = root_block_data['url']
                    if url_id:
                        url_id = TextDB.get_or_none(TextDB.id == url_id)
                        if url_id:
                            url_id.value_set(account, new_url)
                        else:
                            new_url = TextDB()
                            new_url.save()
                            new_url.default_create(value=new_url)
                            root_block_data['url'] = new_url.id
                    else:
                        new_url = TextDB()
                        new_url.save()
                        new_url.default_create(value=new_url)
                        root_block_data['url'] = new_url.id
                else:
                    root_block_data.pop('url', None)
            root_block.data = json.dumps(root_block_data)
            root_block.save()

        return redirect(f'/articles/{article_id}/{block_id}')

    if root_block:
        data = json.loads(root_block.data)
    else:
        data = {}

    text = ''
    url = ''

    if 'text' in data:
        text_id = data['text']
        if text_id:
            text_db = TextDB.get_or_none(TextDB.id == text_id)
            if text_db:
                text = text_db.value_get(account)

    if 'url' in data:
        url_id = data['url']
        if url_id:
            url_db = TextDB.get_or_none(TextDB.id == url_id)
            if url_db:
                url = url_db.value_get(account)

    widgets = [
        Text(
            text='Редактирование:',
            font=Font(size=32, weight=700),
            margin=Margin(down=16),
        )
    ]

    if text and url:
        widgets.append(
            Form(
                widgets=[
                    Text(
                        text='Текст',
                        font=Font(size=14, weight=700),
                    ),
                    InputText(id='new_value', value=text),
                    Text(
                        text='URL',
                        font=Font(size=14, weight=700),
                    ),
                    InputText(id='new_url', value=url),
                    InputButton(text='Сохранить', margin=Margin(top=8)),
                ],
            )
        )
    elif text:
        widgets.append(
            Form(
                widgets=[
                    Text(
                        text='Текст',
                        font=Font(size=14, weight=700),
                    ),
                    InputText(id='new_value', value=text),
                    InputButton(text='Сохранить', margin=Margin(top=8)),
                ],
            )
        )
    elif url:
        widgets.append(
            Form(
                widgets=[
                    Text(
                        text='URL',
                        font=Font(size=14, weight=700),
                    ),
                    InputText(id='new_url', value=url),
                    InputButton(text='Сохранить', margin=Margin(top=8)),
                ],
            )
        )

    interface_html = interface.html_get(widgets=widgets, active='articles')

    return interface_html
