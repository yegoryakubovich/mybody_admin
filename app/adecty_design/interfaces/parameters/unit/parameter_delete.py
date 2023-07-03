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


from flask import request

from app.adecty_design.interface import interface
from app.adecty_design.widgets.header import header_get
from app.adecty_design.widgets.model_deleter_get import model_deleter_get
from app.adecty_design.widgets.model_deleter_post import model_deleter_post
from app.database.models import Parameter

URL_BACK = '/parameters/'


def interface_parameter_delete(parameter: Parameter):
    if request.method == 'POST':
        return model_deleter_post(
            model=parameter,
            url_back=URL_BACK,
        )

    header = header_get(text='Вопрос удален', url_back=URL_BACK)
    widgets = [
        header,
    ]

    widgets += model_deleter_get(url_back=URL_BACK)

    interface_html = interface.html_get(
        widgets=widgets,
        active='parameters',
    )
    return interface_html, 200
