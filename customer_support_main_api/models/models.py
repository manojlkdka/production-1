# -*- coding: utf-8 -*-

from os import access
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError
import requests
import json
import ast


class CustomerSupportSystem(models.Model):
    _name = 'customer.support.main.api'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    _rec_name = 'subject'

    subject = fields.Char(string="Subject",required=True)
    # state = fields.Selection([ ('draft', 'Draft'),('in_progress', 'In Progress'),('closed', 'Closed'),],'Status',default="draft",readonly=True)
    # state = fields.Selection(
        # [('draft', 'Draft'), ('progress', 'Progress'),('closed', 'Closed'),('cancel', 'Cancel')], string='Status',readonly=True default='draft', tracking=True)
    state = fields.Selection([ ('draft', 'Draft'),('in_progress', 'In Progress'),('closed', 'Closed'),('cancel', 'Cancel')],'Delivery Status',readonly=True, default='draft')

    company = fields.Char('Company',readonly=True)
    submitted_user = fields.Char('User',readonly=True)
    module = fields.Char(string="Module Name",readonly=True)
    issue_detail = fields.Html(string="Issue Description",readonly=True)
    attachment = fields.Many2one('ir.attachment',string="Attachment") 
    response_message = fields.Char(string="Response Message",require=True)
    issue_datetime = fields.Char(readonly=True)
    client_url = fields.Char(string="Client Url")
    client_ticket_id = fields.Integer(string="Client Ticket Id")
    client_access_token = fields.Char(string="Client Access Token")


    def create_helpdesk_ticket(self):
        for rec in self:
            rec.state = "in_progress"

    def cancel_helpdesk_ticket(self):
        for rec in self:
            rec.state = "cancel"

    def response_client_helpdesk_ticket(self):
        for rec in self:
            if not rec.response_message:
                raise ValidationError("Please Enter Response Message")
            else:
                # _logger.info("==============================mmmtt========mmmm====%s",main_url)

                end_point = rec.client_url
                client_ticket_id = rec.client_ticket_id
                # if self.attachment.datas:
                    # str_attach = self.attachment.datas.decode("ascii")
                # access_token_obj = self.env['company.token.setup'].search([],limit=1)
                # access_token = access_token_obj.access_token
                access_token = rec.client_access_token
                if end_point:
                    main_url = end_point + "/api/update_support_ticket"

                    _logger.info("======================================mmmm====%s",main_url)
                else:
                    raise ValidationError("Please set the end point in the configuration")
        
                # this_url = self.env['ir.config_parameter'].sudo().get_param('web.base.client.url')
                if access_token:
                    _logger.info("======================================mmmm====%s",access_token)
                    
                    headers = {
                        "access_token": access_token,
                        "content-type": "application/json",
                    }
                else:
                    raise ValidationError("Please set the access token in the configuration")
                try:

                    delivery_response = requests.post(main_url,headers=headers,json={"response_message": rec.response_message,"client_ticket_id": client_ticket_id})
                    _logger.info("=========pppp======%s",delivery_response.content)

                    response_dict = delivery_response.content.decode("utf-8")
                    _logger.info("============dict=======%s===%s",response_dict,type(response_dict))
                    # response_data = ast.literal_eval(response_dict)
                    res = json.loads(response_dict)
                    if res['result']['status'] == 200:
                        rec.write({
                            'state' : 'closed' 
                        }) 

                except Exception as e:
                    _logger.info("================================mye==============%s",e)
                    raise ValidationError("Please set the proper configuration")


    # def send_response_to_branch(self):
    #     end_point = self.env['ir.config_parameter'].sudo().get_param('end_point')
    #     if self.attachment.datas:
    #         str_attach = self.attachment.datas.decode("ascii")

    #     access_token_obj = self.env['company.token.setup'].search([],limit=1)
    #     access_token = access_token_obj.access_token
    #     if end_point:
    #         main_url = end_point + "/api/update_support_ticket"
    #     else:
    #         raise ValidationError("Please set the end point in the configuration")
        
    #     this_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     if access_token:

    #         headers = {
    #             "access_token": access_token,
    #             "content-type": "application/json",
    #         }
    #     else:
    #         raise ValidationError("Please set the access token in the configuration")

        
    #     # "submitted_user": self.submitted_user.name,
        
        
        
        
        
    #     try:
    #         delivery_response = requests.post(main_url,headers=headers,json={"res_id": self.id,"subject": self.subject,"delivery_status": self.delivery_status,"issue_detail": self.issue_detail,"issue_datetime": str(self.issue_datetime),
    #        "company": self.company.name,"submitted_user": self.submitted_user.name,"attachment_title":self.attachment.name, "attachment": str_attach,"mimetype": self.attachment.mimetype, "module":self.module.name,"client_url": this_url,
    #         })
    #         _logger.info("=========pppp======%s",delivery_response)
    #         _logger.info("=========pppp======%s",delivery_response.content)

    #         response_dict = delivery_response.content.decode("utf-8")
    #         _logger.info("============dict=======%s===%s",response_dict,type(response_dict))
    #         # response_data = ast.literal_eval(response_dict)
    #         res = json.loads(response_dict)
    #         _logger.info("============res==========%s",res)


    #         # response_status = str(delivery_response.content['result']['status']) 
    #         # response_content = str(delivery_response.content['result']['delivery_status'])
    #         if res['result']['status'] == 200:
    #             _logger.info("===============ok====")
    #             self.write({
    #                 'delivery_status' : res['result']['delivery_status'] 
    #             }) 

    #     except Exception as e:
    #         raise ValidationError("Please set the proper configuration")
            
    

#     def send_issue_ticket_to_branch(self):
#         current_token = ""
#         if self.client_url:
#             tokenObj = self.env['company.token.setup'].search([('client_url','=',self.client_url)],limit=1)
#             current_token = tokenObj.access_token 
#             main_url = self.client_url + "/api/update_support_ticket"
#             _logger.info("================mainurl===============%s",main_url)
#             if current_token:
#                 headers = {
#                 "access_token": current_token,
#                 "content-type": "application/json",
#             }
#         else:
#             raise ValidationError("Please set the access token in the configuration")

        
        
        
        
        
        
#         try:
#             delivery_response = requests.post(main_url,headers=headers,json={"client_ticket_id": self.client_ticket_id,"response_message": self.response_message})

#             response_dict = delivery_response.content.decode("utf-8")
#             _logger.info("============dict=======%s===%s",response_dict,type(response_dict))
#             res = json.loads(response_dict)


#             if res['result']['status'] == 200:
#                 _logger.info("===============ok====")
             
#         except Exception as e:
#             raise ValidationError("Please set the proper configuration")

class CompanyTokenSetup(models.Model):
    _name = 'company.token.setup'
    _rec_name = 'url_endpoint'

    url_endpoint = fields.Char(string="Url EndPoint",required=True)
    access_token = fields.Char(string="Access Token",readonly=True)

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
                self.write({
                    'access_token' : response_content 
                }) 

        except Exception as e:
            _logger.info("===============e===========%s",e)
            raise ValidationError("Access Token is not generated")
        