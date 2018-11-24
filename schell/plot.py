import matplotlib.pyplot as plt

sizes = [50*50, 100*100, 150*150, 200*200, 250*250, 300*300, 350*350, 400*400]

initialization_times = [0.034, 0.420, 2.050, 6.444, 15.571, 32.180, 59.834, 76.218]
plt.plot(sizes, initialization_times)
plt.title('Initialization Time vs Board Size')
plt.savefig('plot/initialization_time_plot.png')
plt.show()

iterations_times = [0.260, 1.273, 3.179, 5.421, 9.226, 14.366, 21.712, 22.972]
plt.plot(sizes, iterations_times)
plt.title('Iterations Time vs Board Size')
plt.savefig('plot/iterations_time_plot.png')
plt.show()

avg_iteration_times = [0.023, 0.090, 0.206, 0.375, 0.592, 0.855, 1.202, 1.397]
plt.plot(sizes, avg_iteration_times)
plt.title('Average Iteration Time vs Board Size')
plt.savefig('plot/average_iteration_time_plot.png')
plt.show()

total_times = [0.690, 2.251, 6.049, 13.014, 26.430, 48.692, 85.189, 112.457]
plt.plot(sizes, total_times)
plt.title('Total Time vs Board Size')
plt.savefig('plot/total_time_plot.png')
plt.show()

intolerance = [0.05 * i for i in range(1, 18)]
segregation = [51.55, 51.21, 55.23, 57.28, 58.69, 75.76, 77.74, 84.54, 87.76,
               88.46, 93.36, 97.25, 99.14, 99.49, 99.78, 99.73, 99.55]
plt.plot(intolerance, segregation)
plt.title('Segregation vs Intolerance')
plt.savefig('plot/segregation_plot.png')
plt.show()

"""
sizes = ['30x30', '60x60', '120x120', '240x240', '480x480']
times = [0.01, 0.02, 0.09, 0.37, 1.00]
plt.plot(sizes, times)
plt.title('Time per iteration vs Board Size')
plt.show()
"""