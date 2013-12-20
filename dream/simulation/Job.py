# ===========================================================================
# Copyright 2013 University of Limerick
#
# This file is part of DREAM.
#
# DREAM is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DREAM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DREAM.  If not, see <http://www.gnu.org/licenses/>.
# ===========================================================================
'''
Created on 01 Oct 2013

@author: George
'''
'''
Job is an Entity that implements the logic of a job shop. Job carries attributes for its route 
in the system and also in the processing times at each station
'''

from Globals import G
from Entity import Entity

# ============================ The job object ==============================
class Job(Entity):                                  # inherits from the Entity class   
    type="Job"
    
    def __init__(self, id=None, name=None, route=[], priority=0, dueDate=None, orderDate=None, extraPropertyDict=None):
        Entity.__init__(self, id=id,name=name, priority=priority, dueDate=dueDate, orderDate=orderDate)
        # instance specific attributes 
        self.id=id                                  # id
        # information on the routing and the stops of the entity
        self.route=route                            # the route that the job follows, 
                                                    # also contains the processing times in each station
        self.remainingRoute=list(route)                   # the remaining route. in the beginning 
                                                    # this should be the same as the full route
        # the scheduling of the entity as resolved by the simulation
        self.schedule=[]                            # keeps the result of the simulation. 
                                                    # A list with the stations and time of entrance
        self.extraPropertyDict = extraPropertyDict
        
    #==================== outputs results to JSON File ======================
    def outputResultsJSON(self):
        from Globals import G
        if(G.numberOfReplications==1):              #if we had just one replication output the results to excel
            json={}                                 # dictionary holding information related to the specific entity
            json['_class'] = 'Dream.Job'
            json['id'] = str(self.id)
            json['results'] = {}
            json['extraPropertyDict'] = self.extraPropertyDict
            
            #if the Job has reached an exit, input completion time in the results
            if self.schedule[-1][0].type=='Exit':
                json['results']['completionTime']=self.schedule[-1][1]  
                completionTime=self.schedule[-1][1]  
            #else input "still in progress"
            else:
                json['results']['completionTime']="still in progress"  
                completionTime=None
            
            if completionTime and self.dueDate:
                delay=completionTime-self.dueDate
                json['results']['delay']=delay
                
            json['results']['schedule']=[]
            i=0
            for record in self.schedule:               
                json['results']['schedule'].append({})                                  # dictionary holding time and 
                json['results']['schedule'][i]['stepNumber']=i                      #the step number
                json['results']['schedule'][i]['stationId']=record[0].id              # id of the Object
                json['results']['schedule'][i]['entranceTime']=record[1]           # time entering the Object
                i+=1             
            G.outputJSON['elementList'].append(json)
        
    # ==== initializes all the Entity for a new simulation replication ======
    def initialize(self):
        # has to be re-initialized each time a new Job is added
        self.remainingRoute=list(self.route)   
        self.currentStation=self.route[0][0]    

