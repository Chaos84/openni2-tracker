#!/usr/bin/env python

"""
    Convert a skeleton transform tree to a list of visualization markers for RViz.
        
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2011 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.html

    Edited by Robin Rasch, University of Applied Sciences Bielefeld, Germany, www.iot-minden.de
"""

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import tf

class Person():
	head = Point()
	neck = Point()
	torso = Point()
	right_shoulder = Point()
	right_elbow = Point()
	right_hand = Point()
	right_hip = Point()
	right_knee = Point()
	right_foot = Point()
	left_shoulder = Point()
	left_elbow = Point()
	left_hand = Point()
	left_hip = Point()
	left_knee = Point()
	left_foot = Point()

class SkeletonMarkers():
    def __init__(self):
        rospy.init_node('markers_from_tf')
                
        rospy.loginfo("Initializing Skeleton Markers Node...")
        
        rate = rospy.get_param('~rate', 20)
        r = rospy.Rate(rate)
        
        # There is usually no need to change the fixed frame from the default
        self.fixed_frame = rospy.get_param('~fixed_frame', 'camera_frame')
        
        # Get the list of skeleton frames we want to track
        self.skeleton_frames = rospy.get_param('tracker', '')

        # Initialize the tf listener
        tf_listener = tf.TransformListener()
        
        # Define a marker publisher
        marker_pub = rospy.Publisher('skeleton_markers', Marker, queue_size=5)
        
        # Intialize the markers
        self.initialize_markers()
        
        # Make sure we see the openni_depth_frame
        tf_listener.waitForTransform(self.fixed_frame, self.fixed_frame, rospy.Time(), rospy.Duration(60.0))
        
        # A flag to track when we have detected a skeleton
        skeleton_detected = False
        
        # Begin the main loop
        while not rospy.is_shutdown():
            # Set the markers header
            self.markers.header.stamp = rospy.Time.now()
                        
            # Clear the markers point list
            self.markers.points = list()
            
            # Assume we can at least see the head frame               
            frames = [f for f in tf_listener.getFrameStrings() if f.startswith('tracker/user_')]

	    users = {}
                
            # Loop through the skeleton frames
            for frame in frames:
                # We only need the origin of each skeleton frame
                # relative to the fixed frame
                position = Point()
		
                info = frame.split('/')
		print 'Info:', info                    
		print 'Frame:', frame             
                # Get the transformation from the fixed frame
                # to the skeleton frame
                try:
                    (trans, rot)  = tf_listener.lookupTransform(self.fixed_frame, frame, rospy.Time(0))
                    position.x = trans[0]
                    position.y = trans[1]
                    position.z = trans[2]

		    user = Person()
		    if users.has_key(info[1]):
			user = users[info[1]]

		    setattr(user,info[2],position)

		    users[info[1]] = user
		    print user
		                                                                
                    # Set a marker at the origin of this frame
#                    self.markers.points.append(position)
                except: 
                    pass

	    #print users

	    for user in users.values():

		rospy.loginfo("Set Frame %s",user)

		head = user.head
		neck = user.neck
		torso = user.torso

                self.markers.points.append(head)
                self.markers.points.append(neck)

                self.markers.points.append(neck)
                self.markers.points.append(torso)

		r_shoulder = user.right_shoulder
		r_ellbow = user.right_elbow
		r_hand = user.right_hand

                self.markers.points.append(neck)
                self.markers.points.append(r_shoulder)

                self.markers.points.append(torso)
                self.markers.points.append(r_shoulder)

                self.markers.points.append(r_shoulder)
                self.markers.points.append(r_ellbow)

                self.markers.points.append(r_ellbow)
                self.markers.points.append(r_hand)

           	l_shoulder = user.left_shoulder
		l_ellbow = user.left_elbow
		l_hand = user.left_hand


                self.markers.points.append(neck)
                self.markers.points.append(l_shoulder)

                self.markers.points.append(torso)
                self.markers.points.append(l_shoulder)

                self.markers.points.append(l_shoulder)
                self.markers.points.append(l_ellbow)

                self.markers.points.append(l_ellbow)
                self.markers.points.append(l_hand)

		r_hip = user.right_hip
		r_knee = user.right_knee
		r_foot = user.right_foot

                self.markers.points.append(torso)
                self.markers.points.append(r_hip)

                self.markers.points.append(r_hip)
                self.markers.points.append(r_knee)

                self.markers.points.append(r_knee)
                self.markers.points.append(r_foot)

		l_hip = user.left_hip
		l_knee = user.left_knee
		l_foot = user.left_foot


                self.markers.points.append(torso)
                self.markers.points.append(l_hip)

                self.markers.points.append(l_hip)
                self.markers.points.append(l_knee)

                self.markers.points.append(l_knee)
                self.markers.points.append(l_foot)

		self.markers.points.append(l_hip)
                self.markers.points.append(r_hip)		

            # Publish the set of markers
            marker_pub.publish(self.markers)
                              
            r.sleep()
            
    def initialize_markers(self):
        # Set various parameters
        scale = rospy.get_param('~scale', 0.07)
        lifetime = rospy.get_param('~lifetime', 0) # 0 is forever
        ns = rospy.get_param('~ns', 'skeleton_markers')
        id = rospy.get_param('~id', 0)
        color = rospy.get_param('~color', {'r': 0.0, 'g': 1.0, 'b': 0.0, 'a': 1.0})
        
        # Initialize the marker points list
        self.markers = Marker()
        self.markers.header.frame_id = self.fixed_frame
        self.markers.ns = ns
        self.markers.id = id
        self.markers.type = Marker.LINE_LIST
        self.markers.action = Marker.ADD
        self.markers.lifetime = rospy.Duration(lifetime)
        self.markers.scale.x = scale
        self.markers.scale.y = scale
        self.markers.color.r = color['r']
        self.markers.color.g = color['g']
        self.markers.color.b = color['b']
        self.markers.color.a = color['a']
        
if __name__ == '__main__':
    try:
        SkeletonMarkers()
    except rospy.ROSInterruptException:
        pass
