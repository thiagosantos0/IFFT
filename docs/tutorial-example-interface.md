This section of documentaion will contain some information regarding IFFT Web Interface.
The idea here is to give a general idea of which options are available.

![initial_page](https://i.postimg.cc/9FYtFDcg/initial-screen.png)

Here is the list of corrent `features` supported by the UI version:

```
- Output viewer
- Graph viewer
- Settings
```
The content of the files are as follows:

<!--- Detailing each feature -->

## **Output Viewer**
This is the page where you can get access to the tool output in a very intuitive and more visual appealing way.
You should be able to get the same results as showed in terminal, but with the advantage of have a more scalable
way of see the contents.

![output_viewer](https://i.postimg.cc/tRDLZ4RJ/Captura-de-tela-2025-01-20-142536.png)

**Note**: *The default project is the "mock_project", so the [dir_name] parameter was not passed.*

### **Search Tab**
You can use the search tab to filter some files of interest or search for a specific file.
This can be very useful when you have a lot of changes inside IFFT blocks in the same change list.
![search_point](https://i.postimg.cc/26YnDYPN/Captura-de-tela-2025-01-26-104039.png)


### **Modal viewer**
Instead of just show the newly added or removed content for each file, the actual result is
stored inside a modal, for the sake of scalability. You can see the actual result clicking in
the `View Modified Lines` button..
![modal](https://i.postimg.cc/T1KdN7T5/modal.png)

### **Download Metadata**
You can also download the IFFT blocks metadata both by JSON and CSV format.
![download](https://i.postimg.cc/8ccRKSFd/download.png)

<!--- Ending of output viewer section -->

## **Graph Viewer**
This is the page where you can see the current dependcy relation between IFFT blocks in your change list.

![graph-viewer](https://i.postimg.cc/4NypvstB/Captura-de-tela-2025-01-26-105946.png)

It's a very handy way to see the dependencies and it is way easier then verify it through the command line.
The Graph is very interactive with actions such as: zoom in, zoom out, node dragging and others. Feel free to explore!


## **Settings Page**
This page allows you to opt-in and out of IFFT features in very easy way. You can safely toggle between the options
as it has a build-in validation implemented so no worries of breaking things! After you make any changes, the configuration
source will be syncronized with the UI immediately.


![settings](https://i.postimg.cc/tCrt8DFR/Captura-de-tela-2025-01-26-110447.png)


