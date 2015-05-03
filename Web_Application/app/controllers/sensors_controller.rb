class SensorsController < ApplicationController
  def update_temperature
  	user = User.find_by(first_name: params[:fn])
  	user.update_attribute(:temperature, params[:val])
    @temperature = user.temperature
      @light_intensity = user.light_intensity
      @humidity = user.humidity
      @pulse_rate = user.pulse_rate
      @noise_level = user.noise_level
      @light_level = user.light_level
      @fan_level = user.fan_level
    render "parameters"
  end
  

  def update_light_intensity
  	user = User.find_by(first_name: params[:fn])
  	user.update_attribute(:light_intensity, params[:val])
    @temperature = user.temperature
      @light_intensity = user.light_intensity
      @humidity = user.humidity
      @pulse_rate = user.pulse_rate
      @noise_level = user.noise_level
      @light_level = user.light_level
      @fan_level = user.fan_level
    render "parameters"
  end

  def update_humidity
  	user = User.find_by(first_name: params[:fn])
  	user.update_attribute(:humidity, params[:val])
    @temperature = user.temperature
      @light_intensity = user.light_intensity
      @humidity = user.humidity
      @pulse_rate = user.pulse_rate
      @noise_level = user.noise_level
      @light_level = user.light_level
      @fan_level = user.fan_level
    render "parameters"
  end

  def update_pulse_rate
  	user = User.find_by(first_name: params[:fn])
  	user.update_attribute(:pulse_rate, params[:val])
    @temperature = user.temperature
      @light_intensity = user.light_intensity
      @humidity = user.humidity
      @pulse_rate = user.pulse_rate
      @noise_level = user.noise_level
      @light_level = user.light_level
      @fan_level = user.fan_level
    render "parameters"
  end

  def update_noise_level
  	user = User.find_by(first_name: params[:fn])
  	user.update_attribute(:noise_level, params[:val])
    @temperature = user.temperature
    @light_intensity = user.light_intensity
    @humidity = user.humidity
    @pulse_rate = user.pulse_rate
    @noise_level = user.noise_level
    @light_level = user.light_level
    @fan_level = user.fan_level
    render "parameters"
  end

  def parameters
      user = User.find_by(first_name: params[:fn])
      p user
      @temperature = user.temperature
      @light_intensity = user.light_intensity
      @humidity = user.humidity
      @pulse_rate = user.pulse_rate
      @noise_level = user.noise_level
      @light_level = user.light_level
      @fan_level = user.fan_level
  end

  def update_light
    user = User.find_by(first_name: params[:fn])
    user.update_attribute(:light_level, params[:val])
    render nothing: true
  end

  def update_fan
    user = User.find_by(first_name: params[:fn])
    user.update_attribute(:fan_level, params[:val])
    render nothing: true
  end

end
