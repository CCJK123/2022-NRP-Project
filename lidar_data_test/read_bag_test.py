import rosbag
bag = rosbag.Bag('lidar_data_test/2023-01-03-12-19-15.bag')
for topic, msg, t in bag.read_messages():
    print(msg)
bag.close()
