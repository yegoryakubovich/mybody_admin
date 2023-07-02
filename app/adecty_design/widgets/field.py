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


from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, InputText


class FieldType:
    string = 'string'


class Field:
    id: str
    type: str
    name: str
    value: str

    def __init__(self, id: str, name: str, value: str = None, type: str = FieldType.string):
        self.id = id
        self.type = type
        self.name = name
        self.value = value

    def widgets_get(self, is_disabled=False, value: str = None):
        widgets = [
            Text(
                text=self.name,
                font=Font(
                    size=22,
                    weight=500,
                ),
                margin=Margin(top=12),
            ),
        ]

        if self.type == FieldType.string:
            widgets += [
                InputText(
                    id=self.id,
                    value=value if value else self.value,
                    margin=Margin(top=6),
                    is_disabled=is_disabled,
                ),
            ]

        return widgets
