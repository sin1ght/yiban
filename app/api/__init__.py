from flask import Blueprint

api=Blueprint('api',__name__)

from . import post_assessment,user_info,get_assessment,check_pass,check_reject

from .culture import *
from .goods import *
from .place import *