import json
import logging
import webapp2


class Webhook(webapp2.RequestHandler):

    def post(self, event=None):
        logging.info('Webhook received: {0}'.format(event))
        payload = json.loads(self.request.body)
        logging.info('Webhook payload: {0}'.format(payload))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write({'event': event, 'status': 'accepted'})


# our main WSGI app
app = webapp2.WSGIApplication(
    [
        webapp2.Route('/webhook/', Webhook),
        webapp2.Route('/webhook/<event>/', Webhook),
    ],
    debug=True,
)
