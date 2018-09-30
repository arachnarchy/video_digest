import matplotlib.pyplot as plt

def sentiment_plot(score, magnitude, filename):
    ymax = 0.005
    fig, ax = plt.subplots(figsize = (8,1))
    ax.plot([score, score], [0, magnitude], 'k-', lw=8)
    ax.set_ylim([0, ymax])
    ax.set_xlim([-1, 1])

    ax.yaxis.set_visible(False)

    plt.fill([-1,1,1,-1], [0,0,ymax,ymax], 'w', alpha=1)
    plt.fill([-1,0,0,-1], [0,0,ymax,ymax], 'r', alpha=0.1, edgecolor='r')
    plt.fill([1,0,0,1], [0,0,ymax,ymax], 'g', alpha=0.1, edgecolor='r')

    ax.text(-0.95, ymax/3, 'Negative', fontsize=15, color='red', alpha=0.5)
    ax.text(0.75, ymax/3, 'Positive', fontsize=15, color='green', alpha=0.5)

    plt.tight_layout()

    plt.savefig('static/' + filename, transparent=True)
    plt.close()
