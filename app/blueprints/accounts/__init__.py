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

from app.blueprints.accounts.foods_cards import blueprint_foods_cards
from app.blueprints.accounts.trainings_cards import blueprint_trainings_cards
from app.database.models import Account, AccountParameter
from app.decorators.admin_get import admin_get


blueprint_accounts = Blueprint(
    name='blueprint_accounts',
    import_name=__name__,
    url_prefix='/accounts'
)

blueprint_accounts.register_blueprint(blueprint=blueprint_trainings_cards)
blueprint_accounts.register_blueprint(blueprint=blueprint_foods_cards)


@blueprint_accounts.route(rule='/', endpoint='get', methods=['GET'])
@admin_get(not_return=True)
def accounts_get():
    accounts = Account.select()
    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Список аккаунтов',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
            ]
        )
    ]

    account_widgets = []
    for account in accounts:
        new_widget = Card(
            margin=Margin(down=16),
            widgets=[
                Text(text=f"ID: {account.adecty_account_id} \n"
                          f"Имя: {account.first_name} \n "
                          f"Фамилия: {account.last_name} \n",
                     font=Font(size=16)),
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/accounts/{account.id}/edit',
                        ),
                    ],
                ),
            ]
        )
        account_widgets.append(new_widget)

    widgets.extend(account_widgets)

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )
    return interface_html


@blueprint_accounts.route(rule='/<int:account_id>/edit', endpoint='edit', methods=['GET'])
@admin_get(not_return=True)
def account_edit(account_id):
    account = Account.get_or_none(Account.id == account_id)

    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text=f"Редактирование аккаунта: {account.first_name} {account.last_name} ",
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
            ]
        ),
        Button(
            type=ButtonType.chip,
            text='Получить информацию об аккаунте',
            margin=Margin(horizontal=8, right=6),
            url=f'/accounts/{account.id}/info',
        ),
        Button(
            type=ButtonType.chip,
            text='Получить информацию по карте тренировок',
            margin=Margin(horizontal=8, right=6),
            url=f'/accounts/{account.id}/trainings_cards',
        ),
        Button(
            type=ButtonType.chip,
            text='Получить информацию по карте питания',
            margin=Margin(horizontal=8, right=6),
            url=f'/accounts/{account.id}/foods_cards',
        )
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )
    return interface_html


@blueprint_accounts.route('/<int:account_id>/info', endpoint='info', methods=['GET'])
@admin_get(not_return=True)
def info_get(account_id):
    account = Account.get_or_none(Account.id == account_id)

    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Информация об аккаунте',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
            ]
        ),
        Card(
            margin=Margin(down=16),
            widgets=[
                Text(text="Общая информация", font=Font(size=20)),
                Text(text=f"ID: {account.adecty_account_id}\n"
                          f"Имя: {account.first_name}\n"
                          f"Фамилия: {account.last_name}\n"
                          f"Отчество: {account.middle_name}\n"
                          f"Пол: {account.gender}\n"
                          f"Telegram: {account.telegram}\n"
                          f"Часовой пояс: {account.timezone}",
                     font=Font(size=16))
            ]
        ),
        Text(
            text='Анкета',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
    ]

    parameters = AccountParameter.select().where(AccountParameter.account == account)

    if parameters:
        for parameter in parameters:
            parameter_widget = Card(
                margin=Margin(down=16),
                widgets=[
                    Text(text=f"{parameter.value_get(account)}: {parameter.value}", font=Font(size=16))
                ]
            )
            widgets.append(parameter_widget)
    else:
        no_parameters_widget = Card(
            margin=Margin(down=16),
            widgets=[
                Text(text="Нет отвеченных вопросов на анкету", font=Font(size=16))
            ]
        )
        widgets.append(no_parameters_widget)

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )
    return interface_html
