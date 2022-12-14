# Cleaner

## Documentation
### Installation
To use the application, you can simply clone this repository with
`git clone https://github.com/imhassane/cleaner`
or by downloading the repository.

### Usage
Cleaner removes files which has been created or updated in a certain amount of time.
It takes some parameters.

#### Parameters
`--repertory` Repertory to clean  
`--delay` An amount of time of expiry for the files  
`--timeunit` The unit of time. Possible values are: `second | minute | hour | day | month |year`  
`--target` The timestamp of the file to consider. Possible values are: `update | creation`. The default value is `update`.

### Example
`python main.py --repertory Test --delay 10 --timeunit hour --target creation`