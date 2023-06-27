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


from flask import Blueprint

from app.adecty_design.interface import interface
from adecty_design.properties import Font, Margin, Align, AlignType
from adecty_design.widgets import Text, Button, ButtonType, Card, View, ViewType
from app.database.models import OrderTraining
from app.decorators.admin_get import admin_get


blueprint_trainings_cards = Blueprint(
    name='blueprint_trainings_cards',
    import_name=__name__,
    url_prefix='/<int:account_id>/trainings_cards'
)


@blueprint_trainings_cards.route(rule='/', endpoint='get', methods=['GET'])
@admin_get(not_return=True)
def trainings_get(account_id):
    trainings = OrderTraining.select()
    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Карта тренировок',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
                Button(
                    type=ButtonType.chip,
                    text='Создать',
                    url=f'/accounts/{account_id}/trainings_cards/create'
                ),
            ]
        )
    ]

    for training in trainings:
        new_widget = Card(
            margin=Margin(down=16),
            widgets=[
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/accounts/{account_id}/trainings_cards/update',
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/accounts/{account_id}/trainings_cards/delete',
                        ),
                    ],
                ),
                Text(
                    text=f"Название: {training.name}\n"
                         f"Количество: {training.unit}\n"
                         f"Статья: {training.article}",
                    font=Font(size=16)
                )
            ]
        )
        widgets.append(new_widget)

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )

    return interface_html


@blueprint_trainings_cards.route(rule='/create', endpoint='create', methods=['GET'])
@admin_get(not_return=True)
def trainings_create(account_id):
    widgets = [
        Card(
            widgets=[
                Button(
                    text='Добавить упражнение',
                    url=f'/trainings_cards/exercise/create',
                    margin=Margin(down=8)
                ),
                Button(
                    text='Добавить статью',
                    url=f'/trainings_cards/article/create',
                    margin=Margin(down=8)
                )
            ],
            margin=Margin(down=16)
        )
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='account',
    )

    return interface_html
