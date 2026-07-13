from django.db import models
from datetime import datetime
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]
    ticket_number = models.CharField(max_length=20,unique=True,blank=True)
    user = models.ForeignKey("helpdesk_account.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )
    attachment = models.FileField(upload_to='tickets/',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            year = datetime.now().year
            last_ticket = Ticket.objects.filter(
                ticket_number__startswith=f"TKT-{year}"
            ).order_by("-id").first()
            if last_ticket:
                last_number = int(last_ticket.ticket_number.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            self.ticket_number = f"TKT-{year}-{new_number:04d}"
        super().save(*args, **kwargs)
class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        "helpdesk_account.Profile",
        on_delete=models.CASCADE
    )
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created"]
    def __str__(self):
        return f"{self.user.user.username} - {self.ticket.title}"
# Create your models here.
