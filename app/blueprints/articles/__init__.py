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


from flask import Blueprint, request, redirect

from adecty_design.properties import Font, Margin, Align, AlignType
from adecty_design.widgets import Text, InputButton, Button, ButtonType, Form, InputText, Card, View, ViewType
from app.adecty_design.interface import interface
from app.blueprints.articles.arcicle import blueprint_article
from app.database.models import Article, Admin
from app.database import Text as TextDB
from app.decorators.admin_get import admin_get


blueprint_articles = Blueprint(
    name='blueprint_articles',
    import_name=__name__,
    url_prefix='/articles'
)

blueprint_articles.register_blueprint(blueprint=blueprint_article)


@blueprint_articles.route(rule='/', endpoint='get', methods=['GET'])
@admin_get()
def articles_get(admin: Admin):
    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Список статей',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
                Button(
                    type=ButtonType.chip,
                    text='Создать',
                    url='/articles/create'
                ),
            ]
        )
    ]

    for article in Article.select():
        article_text = article.name.value_get(admin.account)
        status_text = 'Отображается' if article.status else 'Не отображается'
        new_widget = Card(
            margin=Margin(down=16),
            widgets=[
                Text(text=f"Название статьи: {article_text}", font=Font(size=16)),
                Text(text=f"Статус: {status_text}", font=Font(size=14)),
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/articles/{article.id}/update',
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/articles/{article.id}/delete',
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Изминить статус',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/articles/{article.id}/status_update',
                        ),
                    ],
                ),
            ]
        )
        widgets.append(new_widget)

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html


@blueprint_articles.route(rule='/create', endpoint='create', methods=['GET', 'POST'])
@admin_get(not_return=True)
def articles_create():
    if request.method == 'POST':
        name = request.form.get('name')

        text = TextDB()
        text.save()
        text.default_create(value=name)

        article = Article(name=text)
        article.save()

        article_id = article.id

        return redirect(f'/articles/{article_id}/update')

    widgets = [
        Text(
            text='Создание статьи',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Название статьи',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='name'),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html


@blueprint_articles.route('/<int:article_id>/status_update', methods=['GET', 'POST'])
@admin_get(not_return=True)
def article_status_update(article_id):
    article = Article.get_or_none(Article.id == article_id)
    if article:
        article.status = not article.status
        article.save()
    return redirect('/articles')
