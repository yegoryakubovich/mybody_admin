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

from app.adecty_design.interfaces import interface
from adecty_design.properties import Font, Margin, Align, AlignType
from adecty_design.widgets import Text, Button, ButtonType, Card, View, ViewType, InputButton, InputText, Form, \
    InputSelect

from app.blueprints.products.product import blueprint_product
from app.database.models import Admin, Product, Article
from app.decorators.admin_get import admin_get
from app.database import Text as TextDB


blueprint_products = Blueprint(
    name='blueprint_products',
    import_name=__name__,
    url_prefix='/products'
)

blueprint_products.register_blueprint(blueprint=blueprint_product)


@blueprint_products.route(rule='/', endpoint='get', methods=['GET'])
@admin_get()
def articles_get(admin: Admin):
    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Список продуктов',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
                Button(
                    type=ButtonType.chip,
                    text='Создать',
                    url='/products/create'
                ),
            ]
        )
    ]

    for products in Product.select():
        product_text = products.name.value_get(admin.account)
        article_text = products.article.name.value_get(admin.account)
        new_widget = Card(
            margin=Margin(down=16),
            widgets=[
                Text(text=f"Название продукта: {product_text}", font=Font(size=16)),
                Text(text=f"Название статьи: {article_text}", font=Font(size=16)),
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text="Редактировать",
                            margin=Margin(horizontal=8, right=6),
                            url=f'/products/{products.id}/update',
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/products/{products.id}/delete',
                        ),
                    ],
                ),
            ]
        )
        widgets.append(new_widget)

    interface_html = interface.html_get(
        widgets=widgets,
        active='products',
    )

    return interface_html


@blueprint_products.route(rule='/create', endpoint='create', methods=['GET', 'POST'])
@admin_get()
def articles_create(admin: Admin):
    if request.method == 'POST':
        name = request.form.get('name')
        article_name = request.form.get('article_name')
        article = Article().get_by_aricle(name=article_name, account=admin.account)

        text = TextDB()
        text.save()
        text.default_create(value=name)

        products = Product(name=text, article=article)
        products.save()

        return redirect('/products')

    articles = Article.select()
    article_options = [article.article_name_get(account=admin.account) for article in articles]
    if not articles:
        error_message = "Сначала необходимо создать статью."
        widgets = [
            Text(
                text=error_message,
                font=Font(
                    size=16,
                    weight=700,
                ),
                margin=Margin(down=16),
            ),
        ]
        interface_html = interface.html_get(
            widgets=widgets,
            active='accounts',
        )
        return interface_html

    widgets = [
        Text(
            text='Создание продукта',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Название продукта',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='name'),
                Text(
                    text='Статья',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputSelect(id='article_name', options=article_options),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='products',
    )

    return interface_html
