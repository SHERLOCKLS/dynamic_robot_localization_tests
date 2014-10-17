#!/usr/bin/python

import roslib
import rospy
import rosbag
import tf
import geometry_msgs.msg
import os
import sys
import argparse


def change_tf(inbag, outbag, source_frame, target_frame, new_source_frame, new_target_frame, invert_tf_matrix):
  print ' Processing input bagfile: %s' % (inbag)
  print 'Writing to output bagfile: %s' % (outbag)
  print '             Changing tfs: [%s -> %s] [%s -> %s]' % (source_frame, target_frame, new_source_frame, new_target_frame)
  print '      Inverting tf matrix: %s' % (invert_tf_matrix)

  outbag = rosbag.Bag(outbag, 'w', rosbag.bag.Compression.BZ2)
  for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
      if topic == '/tf':
          for transform_msg in msg.transforms:
              if transform_msg.header.frame_id == source_frame and transform_msg.child_frame_id == target_frame:
                  transform_msg.header.frame_id = new_source_frame
                  transform_msg.child_frame_id = new_target_frame
                  
                  if invert_tf_matrix:
                      transform_msg.transform.translation.x *= -1.0
                      transform_msg.transform.translation.y *= -1.0
                      transform_msg.transform.translation.z *= -1.0
                      transform_msg.transform.rotation.x *= -1.0
                      transform_msg.transform.rotation.y *= -1.0
                      transform_msg.transform.rotation.z *= -1.0
      outbag.write(topic, msg, t)
  rospy.loginfo('Closing output bagfile and exit...')
  outbag.close();


if __name__ == "__main__":

  parser = argparse.ArgumentParser(
      description='Changes tf frame_ids with the option to invert the tf matrix')
  parser.add_argument('-i', metavar='INPUT_BAGFILE', required=True, help='Input bagfile')
  parser.add_argument('-o', metavar='OUTPUT_BAGFILE', required=True, help='Output bagfile')
  parser.add_argument('-s', metavar='SOURCE_FRAME_ID', required=True, help='Source frame_id')
  parser.add_argument('-t', metavar='TARGET_FRAME_ID', required=True, help='Target frame_id')
  parser.add_argument('-b', metavar='NEW_SOURCE_FRAME_ID', required=True, help='New source frame_id')
  parser.add_argument('-e', metavar='NEW_TARGET_FRAME_ID', required=True, help='New target frame_id')
  parser.add_argument('-m', metavar='INVERT_MATRIX', required=True, help='Invert transformation matrix')
  args = parser.parse_args()

  try:
    change_tf(args.i, args.o, args.s, args.t, args.b, args.e, args.m)
    exit(0)
  except Exception, e:
    import traceback
    traceback.print_exc()
