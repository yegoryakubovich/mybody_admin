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


from adecty_design.properties import Margin
from adecty_design.widgets import InputButton, Form
from peewee import Model

from app.adecty_design.widgets.field import Field


# noinspection PyUnusedLocal
def model_updator_get(fields: list[Field], model: Model):
    form_widgets = []

    for field in fields:
        form_widgets += field.widgets_get(
            value=eval(
                'model.{id}'.format(
                    id=field.id,
                ),
            )
        )

    form_widgets += [
        InputButton(text='Сохранить', margin=Margin(top=12)),
    ]

    widgets = [
        Form(
            widgets=form_widgets,
        ),
    ]

    return widgets
