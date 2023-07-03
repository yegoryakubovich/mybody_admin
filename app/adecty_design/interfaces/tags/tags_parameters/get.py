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


from app.adecty_design.interface import interface
from app.adecty_design.widgets.action import Action
from app.adecty_design.widgets.header import header_get
from app.adecty_design.widgets.models_viewer_get import models_viewer_get
from app.adecty_design.widgets.unit import Unit
from app.database import TagParameter


def interface_tags_parameters_get() -> str:
    header = header_get(text='Теги вопросов к анкете', create_url='/tags_parameter/create')

    widgets = [
        header,
    ]

    widgets += models_viewer_get(
        units=[
            Unit(
                id=tag_parameter.id,
                name='{name}'.format(
                    name=tag_parameter.name,
                ),
                parameters={
                    'Название': tag_parameter.name,
                },
                actions=[
                    Action(
                        name='Редактировать',
                        icon='update.svg',
                        url='/tag_parameters/{id}/update'.format(
                            id=tag_parameter.id,
                        ),
                    ),
                    Action(
                        name='Удалить',
                        icon='delete.svg',
                        url='/tag_parameters/{id}/delete'.format(
                            id=tag_parameter.id,
                        ),
                    ),
                ],
            )
            for tag_parameter in TagParameter.select()
        ],
    )

    interface_html = interface.html_get(
        widgets=widgets,
        active='tags',
    )
    return interface_html
