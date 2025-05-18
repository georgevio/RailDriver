using System.Windows;
using RailDriverDashboard.ViewModels;

namespace RailDriverDashboard
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            DataContext = new RailDriverViewModel();
        }
    }
}