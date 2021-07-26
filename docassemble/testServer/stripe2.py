import stripe
import json
from docassemble.base.util import word, get_config, action_argument, DAObject, prevent_going_back
from docassemble.base.standardformatter import BUTTON_STYLE, BUTTON_CLASS
import requests

webhook_secret = get_config('stripe webhook secret')


__all__ = ['DAStripeCheckOut']


class DAStripeCheckOut(DAObject):
  def init(self, *pargs, **kwargs):
    if get_config('stripe public key') is None or get_config('stripe secret key') is None:
      raise Exception("In order to use a DAStripe object, you need to set stripe public key and stripe secret key in your Configuration.")
    super().init(*pargs, **kwargs)
    if not hasattr(self, 'button_label'):
      self.button_label = "Pay"
    if not hasattr(self, 'button_color'):
      self.button_color = "primary"
    if not hasattr(self, 'error_message'):
      self.error_message = "Please try another payment method."
    self.is_setup = False
  
  def setup(self):
    self.checkout_session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=[
        {
          'price': self.priceId,
          'quantity': 1,
        },
      ],      
      mode='subscription',
      success_url=str(self.success_url),
      cancel_url=str(self.cancel_url),
    )
    float(self.amount)
    str(self.currency)
    self.intent = stripe.PaymentIntent.create(
      amount=int(float('%.2f' % self.amount)*100.0),
      currency=self.currency,
    )
    self.is_setup = True    
    
  @property
  def html(self):
    if not self.is_setup:
      self.setup()
    return """\
<button type="button" class="btn """ + BUTTON_STYLE + self.button_color + " " + BUTTON_CLASS + '"' + """ id="checkout-button">""" + word(self.button_label) + """</button>"""
  
  @property
  def javascript(self):    
    if not self.is_setup:
      self.setup()
    return """\
<script>
  var stripe = Stripe(""" + json.dumps(get_config('stripe public key')) + """);
  var checkoutButton = document.getElementById("checkout-button");
  checkoutButton.addEventListener("click", function () {
    stripe.redirectToCheckout({ sessionId: """ + json.dumps(self.checkout_session.id) + """ });
  });
</script>
    """

  
  @property
  def paid(self):
    if not self.is_setup:
      self.setup()
    if hasattr(self, "payment_successful") and self.payment_successful:
      return True
    if not hasattr(self, 'result'):
      self.demand
    payment_status = stripe.checkout.Session.retrieve(self.checkout_session.id)
    if payment_status.payment_status == 'paid':
      self.payment_successful = True
      return True
    return False
  def process(self):
    self.result = action_argument('result')
    self.paid
    prevent_going_back()