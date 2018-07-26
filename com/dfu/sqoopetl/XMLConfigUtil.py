#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Created on 2018年7月17日
@author: zuiweng.df
'''
from xml_models.xml_models import Model, IntField, CharField, CollectionField


class   ContactInfo1(Model):
    contact_type = CharField(xpath="/contact/@type")
    info = CharField(xpath="/contact/info")
    description = CharField(xpath="/contact/description", default="No description supplied")

class Person(Model):
    id = IntField(xpath="/Person/@id")
    firstName = CharField(xpath="/Person/firstName")
    lastName = CharField(xpath="/Person/lastName")
    contacts = CollectionField(ContactInfo1, order_by="contact_type", xpath="Person/contact-info/contact")





if __name__ == '__main__':
    f=open("D:/workspace/tempsp1/OdsSqoopTool/conf/ptest.xml",'r')
    xmlStr=""
    for line in f.readlines():
        xmlStr=xmlStr+" "+line+"   " 
        
    person = Person(xmlStr)
    print person.lastName