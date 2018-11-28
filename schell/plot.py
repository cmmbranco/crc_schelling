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
segregation = [51.24, 51.19, 55.48, 56.83, 58.02, 75.25, 77.24, 84.15, 88.00,
               88.12, 93.36, 97.22, 97.71, 99.20, 99.78, 99.70, 99.62]
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