# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
import logging
_logger = logging.getLogger(__name__)
import ast
from odoo.exceptions import ValidationError
import base64
class CustomerSupportSystem(models.Model):
    _name = 'customer.support.branch.api'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'subject'



    subject = fields.Char(string="Subject",required=True)
    delivery_status = fields.Selection([ ('draft', 'Draft'),('delivered', 'Delivered'),],'Delivery Status',readonly=True, default='draft')
    company = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id,readonly=True)
    submitted_user = fields.Many2one('res.users','User',default=lambda self: self.env.user,readonly=True)
    module = fields.Many2one('ir.module.module',string="Module Name")
    issue_detail = fields.Html(string="Issue Description")
    attachment = fields.Many2one('ir.attachment',string="Attachment",domain=lambda self: "[('create_uid','=',%s)]" % self.env.user.id)  
    response_message = fields.Char(string="Response Message",readonly=True)
    issue_datetime = fields.Datetime(readonly=True, default=fields.Datetime.now())

    # notes = fields.Html(string="Notes")

    def generate_access_token_client(self):
        this_url = self.env['ir.config_parameter'].sudo().get_param('web.base.ip.url')
        _logger.info("==============this==========%s",this_url)
        if this_url:
            main_url = this_url + "/api/auth/token"

        # authUserObj = self.env['res.users'].search([('login','=',"authentication_user")])
        # _logger.info("================authuser========%s",authUserObj)
        # if not authUserObj:
        #     auth_user = self.env['res.users'].create({
        #     'name': "Authentication User",
        #     'login': 'authentication_user',
        #     "password": "authentication_user_pwd"
        # })

            # _logger.info("===========================db=====%s",self.env.cr.dbname)
        headers = {
                # "content-type": "application/x-www-form-urlencoded",
                "db": str(self.env.cr.dbname),
                'login': "admin",
                'password': "admin"

            }
        # else:
        #     headers = {
        #             # "content-type": "application/x-www-form-urlencoded",
        #             "db": self.env.cr.dbname,
        #             'login': authUserObj.login,
        #             'password': authUserObj.password

        #         }
        try:
            token_response = requests.get(main_url,headers=headers)

            _logger.info("=========pppp======%s",token_response)

            response_dict = token_response.content.decode("utf-8")
            # _logger.info("===================dict======%s",response_dict)
            _logger.info("============dict=======%s===%s",response_dict,type(response_dict))
            # response_data = ast.literal_eval(response_dict)
            # _logger.info("============res==========%s",type(response_data))
            
            res = json.loads(response_dict)
            _logger.info("============restype==========%s===%s",type(res),res)

            response_status = res.get('state') 
            _logger.info("======================st======%s",response_status)
            response_content = str(res.get('access_token'))

            if response_status == "Success":
                # _logger.info("===============ok====")
                return response_content

        except Exception as e:
            _logger.info("===============e===========%s",e)
            raise ValidationError("Access Token is not generated")
        

    def send_issue_ticket_to_main(self):

        end_point = self.env['ir.config_parameter'].sudo().get_param('end_point')
        if self.attachment.datas:
            str_attach = self.attachment.datas.decode("ascii")

        access_token = self.env['ir.config_parameter'].sudo().get_param('access_token')
        if end_point:
            main_url = end_point + "/api/create_support_ticket"
            _logger.info("================mainurl===============%s",main_url)
        else:
            raise ValidationError("Please set the end point in the configuration")
        
        this_url = self.env['ir.config_parameter'].sudo().get_param('web.base.ip.url')
        _logger.info("================thisurl============%s",this_url)
        if access_token:

            headers = {
                "access_token": access_token,
                "content-type": "application/json",
            }
        else:
            raise ValidationError("Please set the access token in the configuration")

        
        # "submitted_user": self.submitted_user.name,
        
        
        
        
        
        try:
            response_token = self.generate_access_token_client()
            _logger.info("===========================response_token=============%s",response_token)
            _logger.info("--------------------------a------------------%s",self.issue_detail)
            delivery_response = requests.post(main_url,headers=headers,json={"access_token":response_token, "res_id": self.id,"subject": self.subject,"delivery_status": self.delivery_status,"issue_detail": self.issue_detail,"issue_datetime": str(self.issue_datetime),
           "company": self.company.name,"submitted_user": self.submitted_user.name,"attachment_title":self.attachment.name, "attachment": str_attach,"mimetype": self.attachment.mimetype, "module":self.module.name,"client_url": this_url,
            })
            _logger.info("=========pppp======%s",delivery_response)
            _logger.info("=========pppp======%s",delivery_response.content)

            response_dict = delivery_response.content.decode("utf-8")
            _logger.info("============dict=======%s===%s",response_dict,type(response_dict))
            # response_data = ast.literal_eval(response_dict)
            res = json.loads(response_dict)
            _logger.info("============res==========%s",res)


            # response_status = str(delivery_response.content['result']['status']) 
            # response_content = str(delivery_response.content['result']['delivery_status'])
            if res['result']['status'] == 200:
                _logger.info("===============ok====")
                self.write({
                    'delivery_status' : res['result']['delivery_status'] 
                }) 

        except Exception as e:
            raise ValidationError("Please set the proper configuration")
            
        