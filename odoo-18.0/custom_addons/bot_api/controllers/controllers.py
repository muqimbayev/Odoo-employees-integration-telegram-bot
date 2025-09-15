# -*- coding: utf-8 -*-
# from odoo import http


# class BotApi(http.Controller):
#     @http.route('/bot_api/bot_api', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bot_api/bot_api/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bot_api.listing', {
#             'root': '/bot_api/bot_api',
#             'objects': http.request.env['bot_api.bot_api'].search([]),
#         })

#     @http.route('/bot_api/bot_api/objects/<model("bot_api.bot_api"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bot_api.object', {
#             'object': obj
#         })

