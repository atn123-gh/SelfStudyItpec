from django.db import models
import subprocess
from django.dispatch import receiver
from django.db.models.signals import post_save

class Feedback(models.Model):
    FEEDBACK_TYPE = (
        ('1', 'Suggestion'),
        ('2', 'Bug'),
        ('3', 'Other'),
    )


    id = models.AutoField(primary_key=True)
    feedback_type = models.CharField(max_length=1, choices=FEEDBACK_TYPE ,default="default")

    email =  models.EmailField(max_length = 100)
    details = models.TextField(max_length=1500) 
    date = models.DateField(auto_now_add=True)

    # def __str__(self):
    #     return self.id
    def __str__(self):
        return str(self.id)
    
backup_file = "feedback.json"

def perform_backup():
    # subprocess.run(['python3', 'manage.py', 'dumpdata', 'home'], stdout=backup_file, text=True)
    output = subprocess.run(
        ['python3', 'manage.py', 'dumpdata', 'home'],
        stdout=subprocess.PIPE,
        text=True
    )

    # Write the output to the backup file
    with open(backup_file, 'w') as bfile:
        bfile.write(output.stdout)

    

    
# Create a signal receiver function
@receiver(post_save, sender=Feedback)
def backup_after_save(sender, instance, created, **kwargs):
    if created:  # To perform the backup only when a new instance is created
        perform_backup()