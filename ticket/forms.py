from django import forms
from .models import Ticket,TicketComment

class Ticketcreateform(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category','priority','attachment']
        help_texts = {
                'description': 'Provide complete details so the IT team can resolve the issue quickly.',
            }
        
class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Write your reply..."
                }
            )
        }