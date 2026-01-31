from .models import *
from .auth import hash_password

def seed(db):
    if db.query(User).count() > 0:
        return
    users = [
        ("admin","admin123","ADMIN"),
        ("manager","manager123","INCIDENT_MANAGER"),
        ("sme","sme123","SME"),
        ("l2","l2123","SUPPORT_L2"),
        ("expert","expert123","SUPPORT_EXPERT")
    ]
    for u,p,r in users:
        db.add(User(username=u,password_hash=hash_password(p),role=r))
    db.add(Bank(name="Demo Bank"))
    db.commit()
