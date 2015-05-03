require 'test_helper'

class SensorsControllerTest < ActionController::TestCase
  test "should get update_temperature" do
    get :update_temperature
    assert_response :success
  end

end
