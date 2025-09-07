namespace WEB_253505.UI.Models;

public class LabViewModel(int labNumber)
{
    public int SelectedId { get; set; }
    public int LabNumber { get; set; } = labNumber;
}