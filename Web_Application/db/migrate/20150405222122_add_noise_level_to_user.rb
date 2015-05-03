class AddNoiseLevelToUser < ActiveRecord::Migration
  def change
    add_column :users, :noise_level, :int
  end
end
