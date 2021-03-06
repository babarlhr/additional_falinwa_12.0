###################################################################################
#
#    Copyright (C) 2017 MuK IT GmbH
#
#    Odoo Proprietary License v1.0
#    
#    This software and associated files (the "Software") may only be used 
#    (executed, modified, executed after modifications) if you have
#    purchased a valid license from the authors, typically via Odoo Apps,
#    or if you have received a written agreement from the authors of the
#    Software (see the COPYRIGHT file).
#    
#    You may develop Odoo modules that use the Software as a library 
#    (typically by depending on it, importing it and using its resources),
#    but without copying any source code or material from the Software.
#    You may distribute those modules under the license of your choice,
#    provided that this license is compatible with the terms of the Odoo
#    Proprietary License (For example: LGPL, MIT, or proprietary licenses
#    similar to this one).
#    
#    It is forbidden to publish, distribute, sublicense, or sell copies of
#    the Software or modified copies of the Software.
#    
#    The above copyright notice and this permission notice must be included
#    in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###################################################################################

import logging

from odoo import _, models, api, fields, SUPERUSER_ID

_logger = logging.getLogger(__name__)

class AuthorizationCode(models.Model):
    
    _name = 'muk_rest.authorization_code'
    _description = "OAuth2 Authorization Code"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    code = fields.Char(
        string="Code",
        required=True,
        readonly=True)
    
    state = fields.Char(
        string="State",
        readonly=True)

    callback = fields.Char(
        string="Callback",
        readonly=True)
    
    user = fields.Many2one(
        comodel_name='res.users',
        string="User",
        readonly=True,
        ondelete='cascade')
    
    oauth = fields.Many2one(
        comodel_name='muk_rest.oauth2',
        string="Configuration",
        required=True, 
        readonly=True,
        ondelete='cascade')
    
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    def _read_from_database(self, field_names, inherited_field_names=[]):
        super(AuthorizationCode, self)._read_from_database(field_names, inherited_field_names)
        protected_fields = ['code', 'state']
        if self.env.uid != SUPERUSER_ID and set(protected_fields).intersection(field_names):
            for record in self:
                for field in protected_fields:
                    try:
                        record._cache[field]
                        record._cache[field] = '****************'
                    except:
                        pass
