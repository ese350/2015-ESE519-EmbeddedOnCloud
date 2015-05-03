class AddPulseRateToUser < ActiveRecord::Migration
  def change
    add_column :users, :pulse_rate, :int
  end
end
