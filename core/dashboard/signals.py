from django.dispatch import receiver
from django.db.models.signals import post_save


from accounts.models import Account
from dashboard.models import Wallet, Disbursement


@receiver(post_save, sender=Account)
def create_wallet(sender, instance, created, **kwargs):
    '''Create a wallet for each new staff member. Also create a wallet for each approved labourer'''
    if created == True:
        if instance.is_staff or instance.is_superuser:
            wallet = Wallet.objects.create(holder=instance)
            wallet.save()
            instance.wallet = wallet
            instance.save()
            print('Wallet created for staff member')
    else:
        if instance.is_labourer or instance.is_staff or instance.is_superuser:
            if not instance.wallet:
                wallet = Wallet.objects.create(holder=instance)
                wallet.save()
                instance.wallet = wallet
                instance.save()
                print('Wallet created for labourer')


@receiver(post_save, sender=Disbursement)
def set_modified_by(sender, instance, created, request, **kwargs):
    '''Set the modified by field to the user who modified the disbursement'''
    if created == False:
        instance.modified_by = request.user
        instance.save()
        print('Modified by set to request.user')
