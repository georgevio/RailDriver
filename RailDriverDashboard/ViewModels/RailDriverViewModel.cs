using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Threading;
using RailDriverDashboard.Services;
using System.Windows.Input;

namespace RailDriverDashboard.ViewModels
{
    public class RailDriverViewModel : INotifyPropertyChanged
    {
        private readonly RailDriverService _railDriverService;
        private DispatcherTimer _timer;
        private string _railDriverConnectionStatus = "DISCONNECTED";
        private string _railSimConnectionStatus = "DISCONNECTED";
        private string _locomotiveName = "Unknown";
        private float _controllerValue;
        private float _currentControllerValue;
        private float _combinedThrottleBrake;
        private float _railSimulatorValue;
        private float _railDriverControllerValue;
        private int _locomotiveChangedFlag;
        private string _locomotiveSetFlag = "N/A";
        private string[] _availableControllersArray = Array.Empty<string>(); // Backing array
        private string _newLocomotiveName = ""; 
        public ICommand SetLocomotiveNameCommand { get; } 

        public event PropertyChangedEventHandler? PropertyChanged; // Make nullable

        public string[] AvailableControllersArray
        {
            get => _availableControllersArray;
            set
            {
                _availableControllersArray = value;
                OnPropertyChanged(nameof(AvailableControllersArray));
            }
        }

        public ObservableCollection<string> ControllerListDisplay { get; } = new ObservableCollection<string>();

        private void UpdateControllerList()
        {
            ControllerListDisplay.Clear();
            Console.WriteLine("Updating ControllerListDisplay..."); // Debug log

            foreach (var controller in _availableControllersArray)
            {
                Console.WriteLine($"Controller: {controller}"); // Debug output
                ControllerListDisplay.Add(controller);
            }

            Console.WriteLine($"Total controllers found: {ControllerListDisplay.Count}");
        }



        public string AvailableControllersRaw => string.Join(", ", _availableControllersArray);

        public string RailDriverConnectionStatus
        {
            get => _railDriverConnectionStatus;
            set
            {
                _railDriverConnectionStatus = value;
                OnPropertyChanged(nameof(RailDriverConnectionStatus));
            }
        }

        public string RailSimConnectionStatus
        {
            get => _railSimConnectionStatus;
            set
            {
                _railSimConnectionStatus = value;
                OnPropertyChanged(nameof(RailSimConnectionStatus));
            }
        }

        public string LocomotiveName
        {
            get => _locomotiveName;
            set
            {
                _locomotiveName = value;
                OnPropertyChanged(nameof(LocomotiveName));
            }
        }

        public string NewLocomotiveName 
        {
            get => _newLocomotiveName;
            set
            {
                _newLocomotiveName = value;
                OnPropertyChanged(nameof(NewLocomotiveName));
            }
        }

        public float ControllerValue
        {
            get => _controllerValue;
            set
            {
                _controllerValue = value;
                OnPropertyChanged(nameof(ControllerValue));
            }
        }

        public float CurrentControllerValue
        {
            get => _currentControllerValue;
            set
            {
                _currentControllerValue = value;
                OnPropertyChanged(nameof(CurrentControllerValue));
            }
        }

        public float CombinedThrottleBrake
        {
            get => _combinedThrottleBrake;
            set
            {
                _combinedThrottleBrake = value;
                OnPropertyChanged(nameof(CombinedThrottleBrake));
            }
        }

        public float RailSimulatorValue
        {
            get => _railSimulatorValue;
            set
            {
                _railSimulatorValue = value;
                OnPropertyChanged(nameof(RailSimulatorValue));
            }
        }

        public float RailDriverControllerValue
        {
            get => _railDriverControllerValue;
            set
            {
                _railDriverControllerValue = value;
                OnPropertyChanged(nameof(RailDriverControllerValue));
            }
        }

        public int LocomotiveChangedFlag
        {
            get => _locomotiveChangedFlag;
            set
            {
                _locomotiveChangedFlag = value;
                OnPropertyChanged(nameof(LocomotiveChangedFlag));
            }
        }

        public string LocomotiveSetFlag
        {
            get => _locomotiveSetFlag;
            set
            {
                _locomotiveSetFlag = value;
                OnPropertyChanged(nameof(LocomotiveSetFlag));
            }
        }

        public ObservableCollection<ControllerValuePair> ControllerValues { get; } = new ObservableCollection<ControllerValuePair>();

        public RailDriverViewModel()
        {
            _railDriverService = new RailDriverService();

            SetLocomotiveNameCommand = new RelayCommand(SetLocomotiveName); // Initialize the command

            _timer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(100)
            };
            _timer.Tick += Timer_Tick;
            _timer.Start();

            FetchInitialData();
        }

        private void FetchInitialData()
        {
            RailDriverConnectionStatus = _railDriverService.inGetRailDriverConnected() == 1 ? "CONNECTED" : "DISCONNECTED";
            RailSimConnectionStatus = _railDriverService.inGetRailSimConnected() == 1 ? "CONNECTED" : "DISCONNECTED";
            LocomotiveName = _railDriverService.inGetLocoName();
            AvailableControllersArray = _railDriverService.inGetControllerList(); // Update the property
            UpdateControllerValues();
        }

        private void Timer_Tick(object? sender, EventArgs e) // Make sender nullable
        {
            _railDriverService.inSetRailDriverConnected(1);

            RailDriverConnectionStatus = _railDriverService.inGetRailDriverConnected() == 1 ? "CONNECTED" : "DISCONNECTED";
            RailSimConnectionStatus = _railDriverService.inGetRailSimConnected() == 1 ? "CONNECTED" : "DISCONNECTED";
            LocomotiveName = _railDriverService.inGetLocoName();
            ControllerValue = _railDriverService.inGetControllerValue("SimpleThrottle"); // Example
            CurrentControllerValue = _railDriverService.inGetCurrentControllerValue();
            CombinedThrottleBrake = _railDriverService.inGetRailSimCombinedThrottleBrake();
            RailSimulatorValue = _railDriverService.inGetRailSimValue(); 
            RailDriverControllerValue = _railDriverService.inGetRailDriverValue();
            LocomotiveChangedFlag = _railDriverService.inGetRailSimLocoChanged();
            LocomotiveSetFlag = _railDriverService.inIsLocoSet() == 1 ? "TRUE" : (_railDriverService.inIsLocoSet() == 0 ? "FALSE" : "N/A");
            AvailableControllersArray = _railDriverService.inGetControllerList(); // Update the property
            UpdateControllerValues();
        }

        private void UpdateControllerValues()
        {
            ControllerValues.Clear();
            foreach (var controllerName in _availableControllersArray)
            {
                float value = _railDriverService.inGetControllerValue(controllerName);

                // Debug log to check if the controller name is being processed correctly
                Console.WriteLine($"Querying Controller: {controllerName}, Received Value: {value}");

                ControllerValues.Add(new ControllerValuePair { Name = controllerName, Value = value });
            }
        }



        private void SetLocomotiveName(object parameter)
        {
            _railDriverService.inSetLocoName(_newLocomotiveName);
            LocomotiveName = _railDriverService.inGetLocoName();
            NewLocomotiveName = ""; // Clear the input after setting
        }

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    public class ControllerValuePair
    {
        public string Name { get; set; }
        public float Value { get; set; }
    }

    // Implement a simple ICommand (RelayCommand)
    public class RelayCommand : ICommand
    {
        private readonly Action<object> _execute;
        private readonly Predicate<object> _canExecute;

        public RelayCommand(Action<object> execute, Predicate<object> canExecute = null)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public event EventHandler? CanExecuteChanged
        {
            add => CommandManager.RequerySuggested += value;
            remove => CommandManager.RequerySuggested -= value;
        }

        public bool CanExecute(object parameter)
        {
            return _canExecute == null || _canExecute(parameter);
        }

        public void Execute(object parameter)
        {
            _execute(parameter);
        }
    }
}