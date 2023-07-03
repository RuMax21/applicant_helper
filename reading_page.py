import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

browser = webdriver.Firefox()
browser.get('https://rating.cchgeu.ru/')

def select_level_of_eduvation(value_level_education):
	select = Select(browser.find_element('xpath', '//*[@id="PK"]'))
	select.select_by_visible_text(value_level_education)

def select_form_of_training(value_form_of_training):
	select = Select(browser.find_element('xpath', '//*[@id="learningForm"]'))
	select.select_by_visible_text(value_form_of_training)

def select_faculty(value_faculty):
	select = Select(browser.find_element('xpath', '//*[@id="faculty"]'))
	select.select_by_visible_text(value_faculty)

def select_basis_of_admission(value_basis_of_admission):
	select = Select(browser.find_element('xpath', '//*[@id="osn"]'))
	select.select_by_visible_text(value_basis_of_admission)

def select_type_of_set(value_type_of_set):
	select = Select(browser.find_element('xpath', '//*[@id="nabor"]'))
	select.select_by_visible_text(value_type_of_set)

def select_direction_of_training(value_direction_of_training):
	select = Select(browser.find_element('xpath', '//*[@id="concgrp"]'))
	select.select_by_visible_text(value_direction_of_training)

def builder_of_function(value_level_education, value_form_of_training, value_faculty, value_basis_of_admission, value_type_of_set, value_direction_of_training):
	select_level_of_eduvation(value_level_education)
	select_form_of_training(value_form_of_training)
	select_faculty(value_faculty)
	select_basis_of_admission(value_basis_of_admission)
	select_type_of_set(value_type_of_set)
	select_direction_of_training(value_direction_of_training)
