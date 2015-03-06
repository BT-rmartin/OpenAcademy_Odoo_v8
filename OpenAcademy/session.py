# b-*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 brain-tec AG (http://www.brain-tec.ch)
#    All Right Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields
from openerp.exceptions import Warning
from openerp import tools, api

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Integer(help="Duration in days")
    seats = fields.Integer(string="Number of Seats")
    
    # link sessions to courses and instructors
    course = fields.Many2one('openacademy.course', required=True)
    instructor = fields.Many2one('res.partner')
    
    # link sessions to partners for attendee subscription:
    attendees = fields.Many2many('res.partner')
    
    # example of computed (functional) field
    taken_seats = fields.Float(compute='_compute_taken_seats',string='Percentage of Taken Seats')

    # example of how to set default values
    active = fields.Boolean(default=True)
    start_date = fields.Date(default=fields.Date.today)

    @api.one
    @api.depends('attendees', 'seats')
    def _compute_taken_seats(self):
        if self.seats:
            self.taken_seats = 100.0 * len(self.attendees) / self.seats
        else:
            self.taken_seats = 0.0
        
        # To show that self is a recordset with an hybrid concept: 
        # it is at the same time collection of records and a record

        for session in self:
            print session.name
            print session.course.name
        
        assert self.name == self[0].name
    
    # example of onchange
     
    @api.onchange('course')
    def _onchange_course(self):
        if not self.name:
            self.name = self.course.name     

    # example of constraint
                
    @api.one
    @api.constrains('instructor', 'attendees')
    def _check_instructor(self):
        if self.instructor in self.attendees:
            raise Warning("Instructor of session '%s' "
                "cannot attend its own session" % self.name)

